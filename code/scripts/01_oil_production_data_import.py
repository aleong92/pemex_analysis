#####################################################################
# 01 - OIL PRODUCTION DATA IMPORT PROCESS
# Author: Álvaro León G.
# Undergrad Thesis
# ITAM
#####################################################################
# Libraries
import pandas as pd
import os
import sys
from pathlib import Path

# Append config to system path and import SIH dictionaries
BASE_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BASE_DIR))
from config.config import SIH_DTYPES, SIH_PROD_NAMES

# Define PATH and get file names in the folder
DATA_PATH = BASE_DIR / "data" / "raw"
PROD_FILENAMES = sorted(DATA_PATH.glob("prod_*.csv"))

# Load data and concat into a single dataframe
df = (
    pd
    .concat(
        [
            pd
            .read_csv(
                f,
                encoding='latin-1',
                skiprows=10,
                dtype=SIH_DTYPES,
                parse_dates=['Fecha'],
                date_format="%d-%m-%Y"
            )
            for f in PROD_FILENAMES
        ],
        ignore_index=True
    )
)

# Assign column names
df.rename(columns=SIH_PROD_NAMES, inplace=True)

# Rename oil basins and erase whitespace
df.loc[df['cuenca'] == 'CINTURON PLEGADO DE CHIAPAS', 'cuenca'] = 'CHIAPAS'
df.loc[df['cuenca'] == 'CUENCAS DEL SURESTE', 'cuenca'] = 'SURESTE'
df.loc[df['nombre_pozo'] == 'EL TREINTA-13DES', 'nombre_pozo'] = 'ELTREINTA-13DES'

# Initial well count
print(f"""
      OIL PRODUCTION DATABASE
      -----------------------

      Wells:      {df['nombre_pozo'].nunique():>7,}
      Basins:     {df['cuenca'].nunique():>7,}

      -------------------

      Starts:     {(df['fecha'].dt.year).min():>7}
      Ends:       {(df['fecha'].dt.year).max():>7}
""")

# Drop duplicates based on well name and month
df.drop_duplicates(subset=['nombre_pozo', 'fecha'], keep='first', inplace=True)

# Save dataframe
OUTPUT_DIR = os.path.join("..", "..", "data", "intermediate")
os.makedirs(OUTPUT_DIR, exist_ok=True)
df.to_csv(os.path.join(OUTPUT_DIR, "01_oil_prod.csv"), sep=',', index=False)
