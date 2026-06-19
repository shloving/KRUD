from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

DATA_DIR = Path("DATA")


def detect_header(path: Path) -> int:
    """Guess the correct row to use as headers for this CSV format."""
    try:
        with path.open("r", encoding="utf-8-sig", errors="ignore") as f:
            first_lines = [line.strip() for _, line in zip(range(3), f)]

        if any("Data Entry Initials" in line for line in first_lines):
            return first_lines.index(next(line for line in first_lines if "Data Entry Initials" in line))
        if any("DateTime_Landed" in line for line in first_lines):
            return first_lines.index(next(line for line in first_lines if "DateTime_Landed" in line))
    except Exception:
        pass
    return 0


def safe_columns(cols):
    return [c for c in cols if c is not None and str(c) not in {"nan", "None", "<NA>"}]


@st.cache_data(show_spinner=False)
def load_dataset(path: Path) -> pd.DataFrame:
    header = detect_header(path)
    df = pd.read_csv(path, header=header, dtype=str, skip_blank_lines=True)
    # Keep only real columns (exclude any malformed/unnamed placeholders)
    df = df.loc[:, ~df.columns.astype(str).str.startswith("Unnamed")]
    df = df.rename(columns=lambda c: str(c).strip())

    # Normalize common column names
    rename_map = {
        "Total_Bin_Weight": "Total_Bin_Weight",
        "Total Bin Weight": "Total_Bin_Weight",
        "wet_weight": "wet_weight",
        "wet weight": "wet_weight",
        "diameter": "diameter",
        "height": "height",
        "gonad_weight": "gonad_weight",
        "gonad weight": "gonad_weight",
        "Diver ID": "Diver ID",
        "Vessel ID": "Vessel ID",
        "DateTime_Landed": "DateTime_Landed",
        "DateTime_Processed": "DateTime_Processed",
    }
    df = df.rename(columns=rename_map)

    # Convert obvious numeric columns
    numeric_candidates = [
        "Total_Bin_Weight",
        "Subsample_Weight",
        "wet_weight",
        "diameter",
        "height",
        "gonad_weight",
        "Count",
        "Bin #",
        "Block_Number",
    ]
    for col in numeric_candidates:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Parse date columns when possible
    for col in ["DateTime_Landed", "DateTime_Processed", "Date"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    # Keep a clean display for categorical fields
    for col in df.columns:
        if df[col].dtype == object:
            df[col] = df[col].astype(str).replace({"nan": np.nan, "None": np.nan})

    return df


def main():
    st.set_page_config(page_title="KRUD Dashboard", layout="wide")
    st.title("KRUD Urchin Data Dashboard")

    csv_files = sorted(DATA_DIR.glob("*.csv"))
    if not csv_files:
        st.error("No CSV files were found in the DATA folder.")
        return

    selected_file = st.sidebar.selectbox("Dataset", csv_files, format_func=lambda p: p.name)
    df = load_dataset(selected_file)

    # Column selection helpers
    numeric_cols = safe_columns(
        [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
    )
    date_cols = safe_columns(
        [c for c in ["DateTime_Landed", "DateTime_Processed"] if c in df.columns]
    )
    categorical_cols = safe_columns(
        [
            c
            for c in df.columns
            if c not in numeric_cols and c not in date_cols
        ]
    )

    response_options = safe_columns(
        [
            c
            for c in [
                "Total_Bin_Weight",
                "wet_weight",
                "diameter",
                "height",
                "gonad_weight",
            ]
            if c in df.columns
        ]
    )
    if not response_options:
        st.error("No supported response variables were found in the selected dataset.")
        return

    response_var = st.sidebar.selectbox(
        "Response variable",
        options=response_options,
    )

    candidate_explanatories = safe_columns(
        [
            c
            for c in [
                "Diver ID",
                "Vessel ID",
                "Site_County",
                "Species",
                "Catch_Type",
                "restoration",
                "Data_Flag",
            ]
            if c in df.columns
        ]
    )
    if not candidate_explanatories:
        candidate_explanatories = [c for c in categorical_cols if c != response_var]

    if "Diver ID" in candidate_explanatories:
        default_expl = "Diver ID"
    elif "Vessel ID" in candidate_explanatories:
        default_expl = "Vessel ID"
    else:
        default_expl = candidate_explanatories[0]

    explanatory_var = st.sidebar.selectbox(
        "Explanatory variable",
        options=candidate_explanatories,
        index=(candidate_explanatories.index(default_expl) if default_expl in candidate_explanatories else 0),
    )

    time_options = safe_columns(
        [
            c for c in ["DateTime_Landed", "DateTime_Processed"] if c in df.columns
        ]
    )
    if not time_options:
        time_options = safe_columns(
            [c for c in df.columns if c.lower().endswith("date") or "date" in c.lower()]
        )

    if time_options:
        time_col = st.sidebar.selectbox("Time axis", options=time_options)
    else:
        time_col = None

    agg_method = st.sidebar.radio("Aggregation", ["mean", "median", "sum", "count"], horizontal=True)

    if response_var not in df.columns:
        st.error(f"Selected response variable '{response_var}' is not available in the dataset.")
        return

    if explanatory_var not in df.columns:
        st.error(f"Selected explanatory variable '{explanatory_var}' is not available in the dataset.")
        return

    if time_col is None or time_col not in df.columns or df[time_col].isna().all():
        st.warning(
            "No usable time column was found. Falling back to row order for plotting."
        )
        df = df.reset_index().rename(columns={"index": "row_index"})
        time_col = "row_index"

    plot_df = df[[time_col, explanatory_var, response_var]].copy()
    plot_df = plot_df.dropna(subset=[time_col, explanatory_var, response_var])
    plot_df[time_col] = pd.to_datetime(plot_df[time_col], errors="coerce")
    plot_df = plot_df.dropna(subset=[time_col])

    if plot_df.empty:
        st.warning("No usable rows remain after filtering.")
        return

    plot_df = plot_df.sort_values(by=time_col)

    if pd.api.types.is_datetime64_any_dtype(plot_df[time_col]):
        plot_df["time_bin"] = plot_df[time_col].dt.floor("D")
    else:
        plot_df["time_bin"] = plot_df[time_col]

    summary = (
        plot_df.groupby(["time_bin", explanatory_var], dropna=False)[response_var]
        .agg(agg_method)
        .reset_index()
    )

    col1, col2, col3 = st.columns(3)
    col1.metric("Rows analyzed", f"{len(df):,}")
    col2.metric("Unique groups", f"{summary[explanatory_var].nunique():,}")
    col3.metric(
        "Mean response",
        f"{summary[response_var].mean():.3f}" if agg_method == "mean" else f"{summary[response_var].mean():.3f}",
    )

    fig_line = px.line(
        summary,
        x="time_bin",
        y=response_var,
        color=explanatory_var,
        markers=True,
        title=f"{response_var} over time by {explanatory_var}",
    )
    fig_line.update_layout(template="plotly_white")
    st.plotly_chart(fig_line, use_container_width=True)

    fig_box = px.box(
        plot_df,
        x=explanatory_var,
        y=response_var,
        color=explanatory_var,
        points="outliers",
        title=f"Distribution of {response_var} by {explanatory_var}",
    )
    fig_box.update_layout(template="plotly_white")
    st.plotly_chart(fig_box, use_container_width=True)

    st.subheader("Filtered data preview")
    st.dataframe(plot_df.head(200), use_container_width=True)


if __name__ == "__main__":
    main()
