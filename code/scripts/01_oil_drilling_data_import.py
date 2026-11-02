#####################################################################
# 01 - OIL DRILLING DATA IMPORT PROCESS
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
from config.config import CNH_MAP_DTYPES, CNH_MAP_NAMES

# Define PATH and get file names in the folder
DATA_PATH = BASE_DIR / "data" / "raw"
PERF_FILENAMES = sorted(DATA_PATH.glob("drill_*.csv"))

# Load data and concat into a single dataframe
df = (
    pd
    .concat(
        [
            pd
            .read_csv(
                f,
                encoding='utf-8-sig',
                dtype=CNH_MAP_DTYPES
            )
            for f in PERF_FILENAMES
        ],
        ignore_index=True
    )
)

# Assign column names
df.rename(columns=CNH_MAP_NAMES, inplace=True)

# Parse dates to the correct format
df['fecha_inicio'] = pd.to_datetime(df['fecha_inicio'], format='%d/%m/%Y')
df['fecha_fin'] = pd.to_datetime(df['fecha_fin'], format='%d/%m/%Y')

# Drop duplicates
df.drop_duplicates(subset=['nombre_pozo'], keep='last', inplace=True)

# Initial well count
print(f"""
      OIL WELLS DATABASE
      ------------------

      Rows:       {len(df):>7,}
      Wells:      {df['nombre_pozo'].nunique():>7,}

""")

# Save dataframe
OUTPUT_DIR = os.path.join("..", "..", "data", "intermediate")
os.makedirs(OUTPUT_DIR, exist_ok=True)
df.to_csv(os.path.join(OUTPUT_DIR, "01_oil_drill.csv"), sep=',', index=False)
