#####################################################################
# 02 - OIL WELL INVENTORY
# Author: Álvaro León G.
# Undergrad Thesis
# ITAM
#####################################################################
# Libraries
import pandas as pd
import os
import sys
import numpy as np
from pathlib import Path

# Append config to system path and import SIH dictionaries
BASE_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BASE_DIR))
from config.config import CNH_HC_TYPE

# Import production data
DATA_PATH = BASE_DIR / "data" / "intermediate"
df = (
    pd
    .read_csv(
        os.path.join(DATA_PATH, '01_oil_prod.csv'),
        usecols=['fecha', 'cuenca', 'nombre_pozo', 'petroleo_mbd']
    )
    .groupby(
        ['nombre_pozo'],
        as_index=False
    )
    .agg(
        production_start=('fecha', 'min'),
        basin_name=('cuenca', 'first'),
        total_prod=('petroleo_mbd', 'sum')
    )
)

# Merge with SIH data
df = (
    df
    .merge(
        pd.read_csv(
            os.path.join(DATA_PATH, '01_oil_drill.csv'),
            usecols=['nombre_pozo', 'tipo_hidrocarburo', 'ubicacion']
        ),
        on='nombre_pozo',
        how='left'
    )
)

# Locate oil wells based on hydrocarbon type
df['oil_well'] = df['tipo_hidrocarburo'].map(CNH_HC_TYPE)

# ID remaining ones
OIL_PRODUCERS = df[df['total_prod'] > 0]['nombre_pozo'].tolist()
PENDING_WELLS = df[df['oil_well'].isna()]['nombre_pozo'].tolist()
df['oil_well'] = (
    np
    .select(
        [
            df['nombre_pozo'].isin(OIL_PRODUCERS) & df['nombre_pozo'].isin(PENDING_WELLS)
        ],
        [
            1
        ],
        default=df['oil_well']
    )
)

# Filter oil wells between 1970 and 2018
df = df.query("production_start >= '1970-01-01' and production_start < '2019-01-01'")
df = df.query("oil_well == 1")
(
    print(
        f"""
        WELLS IN INVENTORY:    {df['oil_well'].sum():,.0f}
        """
    )
)

# Identify preexistent wells
df['preexistent_well'] = np.where(df['production_start'] < '2000-01-01', 1, 0)

# Save dataframe
OUTPUT_DIR = os.path.join("..", "..", "data", "intermediate")
os.makedirs(OUTPUT_DIR, exist_ok=True)
df.to_csv(os.path.join(OUTPUT_DIR, "01_well_inventory.csv"), sep=',', index=False)
