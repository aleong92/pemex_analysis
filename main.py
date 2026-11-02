#####################################################################
# MAIN SCRIPT
# Author: Álvaro León G.
# Undergrad Thesis
# ITAM
#####################################################################
# Libraries
import subprocess
import os
import sys

# Define base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Define PATH to scripts
PATH = os.path.join(BASE_DIR, 'code', 'scripts')

# List with scripts ordered by sequential execution
SCRIPTS = [
    '01_oil_prices_wti_data_import.py',
    '01_oil_prices_cpi_data_import.py',
    '01_oil_prices_futures_4m_data_import.py',
    '01_oil_production_data_import.py',
    '01_oil_drilling_data_import.py',
    '01_oil_operator_data_import.py',
    '01_oil_well_inventory.py',
    '02_oil_prices_dataframe.py',
    '02_oil_production_dataframe.py',
    '02_oil_drilling_dataframe.py'
]

# Execute
for s in SCRIPTS:
    print(f"Executing {s}...", flush=True)

    subprocess.run(
        [sys.executable, os.path.join(PATH, s)],
        cwd=PATH,
        check=True
    )

    print(f"Finished executing {s}", flush=True)

print("All scripts executed succesfully.")
