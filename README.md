# KRUD
Kelp Restoration Urchin Demographics (KRUD) is a python project for analyzing and visualizing Purple Sea Urchin (Strongylocentrotus purpuratus) catch data.

## Running the dashboard

1. Activate the project virtual environment:
   ```bash
   source .venv/bin/activate
   ```
2.  Install the required Python packages:
   ```bash
    pip install -r requirements.txt
   ```
3. Start the dashboard:
   ```bash
   streamlit run app.py
   ```
4. Open the local URL shown by Streamlit in your browser (usually http://localhost:8501).

## Dashboard features

- Explore response variables such as `Total_Bin_Weight`, `wet_weight`, `diameter`, `height`, and `gonad_weight`
- Compare trends over time for different explanatory variables such as `Diver ID` and `Vessel ID`

