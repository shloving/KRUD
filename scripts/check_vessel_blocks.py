from pathlib import Path
import sys
import pandas as pd

# Ensure project root is on sys.path so we can import app
sys.path.insert(0, str(Path('.').absolute()))
import app

DATA_DIR = Path('DATA')
paths = sorted(DATA_DIR.glob('*.csv'))
found_any = False
for p in paths:
    try:
        df = app.load_dataset(p)
    except Exception as e:
        print(f"Failed to load {p}: {e}")
        continue

    # Determine relevant columns
    if 'DateTime_Landed' in df.columns:
        date_col = 'DateTime_Landed'
    elif 'DateTime_Processed' in df.columns:
        date_col = 'DateTime_Processed'
    elif 'Date' in df.columns:
        date_col = 'Date'
    else:
        continue

    site_col = 'Portuguese' if 'Portuguese' in df.columns else ('Site_County' if 'Site_County' in df.columns else None)

    tmp = df.dropna(subset=['Vessel ID', 'Block_Number', date_col]).copy()
    if tmp.empty:
        continue
    tmp[date_col] = pd.to_datetime(tmp[date_col], errors='coerce')
    tmp = tmp.dropna(subset=[date_col])
    tmp['time_bin'] = tmp[date_col].dt.floor('D')

    grouped = (
        tmp.groupby(['time_bin', 'Block_Number'])
        .agg(vessels=('Vessel ID', lambda s: sorted(pd.Series(s).dropna().astype(str).unique())),
             vessels_count=('Vessel ID', lambda s: pd.Series(s).dropna().astype(str).nunique()),
             site_val=(site_col, 'first') if site_col is not None else ('Vessel ID', 'first'))
        .reset_index()
    )

    multi = grouped[grouped['vessels_count'] > 1]
    if not multi.empty:
        found_any = True
        print(f"File: {p.name}")
        for _, row in multi.iterrows():
            date = row['time_bin'].date()
            block = row['Block_Number']
            site = row['site_val'] if site_col is not None else ''
            vessels = ', '.join(row['vessels']) if isinstance(row['vessels'], (list, tuple)) else str(row['vessels'])
            print(f"{date} | Site: {site} | Block: {block} | Vessels: {vessels}")

if not found_any:
    print('No days with multiple vessels per block found.')
