#####################################################################
# 02 - OIL PRODUCTION DATAFRAME
# Author: Álvaro León G.
# Undergrad Thesis
# ITAM
#####################################################################
# Libraries
import pandas as pd
import os
from pathlib import Path

# Import production data
BASE_DIR = Path(__file__).resolve().parents[2]
DATA_PATH = BASE_DIR / "data" / "intermediate"
df = (
    pd
    .read_csv(
        os.path.join(DATA_PATH,'01_oil_prod.csv'),
        usecols=['fecha', 'cuenca', 'nombre_pozo', 'petroleo_mbd'],
        parse_dates=['fecha'],
        date_format='%Y-%m-%d'
    )
)

# List of identified oil wells
inv = (
    pd
    .read_csv(
        os.path.join(DATA_PATH,'01_well_inventory.csv'),
        usecols=['nombre_pozo', 'production_start', 'preexistent_well']
    )
)
PREEX_WELLS = inv[inv['preexistent_well'] == 1]['nombre_pozo'].unique().tolist()

# Filter production from oil wells
df = df[df['nombre_pozo'].isin(PREEX_WELLS)].copy()

# Observations from 2000 to 2018
df = df.query("fecha > '1999-12-01' and fecha < '2019-01-01'")

# Save dataframe
OUTPUT_DIR = os.path.join("..", "..", "data", "processed")
os.makedirs(OUTPUT_DIR, exist_ok=True)
df.to_csv(os.path.join(OUTPUT_DIR, "02_oil_production_per_well.csv"), sep=',', index=False)
