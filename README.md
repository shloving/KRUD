# KRUD

Kelp Restoration Urchin Demographics (KRUD) is a Python project for analyzing and visualizing Purple Sea Urchin (*Strongylocentrotus purpuratus*) catch data.

## Prerequisites

Before running the app, make sure you have Python installed:

- Python 3.9 or newer
- A terminal or command prompt
- Internet access to install the Python packages listed in the requirements file

## Running the Dashboard

Open a terminal in the project root folder (the folder that contains this README file and the app.py file).

### macOS

1. Create a virtual environment:

   ```bash
   python3 -m venv .venv
   ```

2. Activate the virtual environment:

   ```bash
   source .venv/bin/activate
   ```

3. Upgrade pip:

   ```bash
   python -m pip install --upgrade pip
   ```

4. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

5. Start the dashboard:

   ```bash
   streamlit run app.py
   ```

6. Open the local URL shown by Streamlit in your browser (usually http://localhost:8501).

7. To stop the app, press Ctrl+C in the terminal.

### Windows

1. Open PowerShell or Command Prompt in the project root folder.

2. Create a virtual environment:

   In PowerShell:

   ```powershell
   py -3 -m venv .venv
   ```

   In Command Prompt:

   ```bat
   py -3 -m venv .venv
   ```

3. Activate the virtual environment:

   In PowerShell:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks the script, run this once and then try again:

   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   ```

   In Command Prompt:

   ```bat
   .venv\Scripts\activate.bat
   ```

4. Upgrade pip:

   ```bat
   python -m pip install --upgrade pip
   ```

5. Install the required Python packages:

   ```bat
   pip install -r requirements.txt
   ```

6. Start the dashboard:

   ```bat
   streamlit run app.py
   ```

7. Open the local URL shown by Streamlit in your browser (usually http://localhost:8501).

8. To stop the app, press Ctrl+C in the terminal.

### If you are running from a fresh clone

If this is the first time you are opening the project, you may need to install Python first and then run the setup steps above from the project folder.

## Dashboard Features

- Explore response variables such as `Total_Bin_Weight`, `wet_weight`, `diameter`, `height`, and `gonad_weight`.
- Compare trends over time for explanatory variables such as `Diver ID` and `Vessel ID`.

