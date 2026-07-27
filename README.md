# KRUD

Kelp Restoration Urchin Demographics (KRUD) is a Python project for analyzing and visualizing Purple Sea Urchin (*Strongylocentrotus purpuratus*) catch data.

## Running the Dashboard

1. Creating the virtual environment:

   ```bash
   python3 -m venv . venv
   ```

2. Activate the project virtual environment:

   ```bash
   source .venv/bin/activate
   ```

3. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Start the dashboard:

   ```bash
   streamlit run app.py
   ```

4. Open the local URL shown by Streamlit in your browser (usually <http://localhost:8501>).

## Dashboard Features

- Explore response variables such as `Total_Bin_Weight`, `wet_weight`, `diameter`, `height`, and `gonad_weight`.
- Compare trends over time for explanatory variables such as `Diver ID` and `Vessel ID`.

