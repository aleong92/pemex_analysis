#####################################################################
# 04 - AVERAGE OIL PRODUCTION
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
DATA_PATH = BASE_DIR / "data" / "processed"
df = (
    pd
    .read_csv(
        os.path.join(DATA_PATH, '02_oil_production_per_well.csv'),
        dtype={
            'nombre_pozo': str,
            'cuenca': str,
            'petroleo_mbd': float
        }
    )
)

# Change oil production from thousand barrels to barrels
df['oil_prod'] = df['petroleo_mbd'] * 1000

# List of wells with no more than 5 years of missing observations
obs_per_well = (
    df['nombre_pozo']
    .value_counts()
    .reset_index()
    .rename(
        columns={'count': 'n_obs'}
    )
)
y5_wells = (
    obs_per_well[obs_per_well['n_obs'] >= 168]['nombre_pozo']
    .tolist()
)

# Build a joint dataframe
av_prod = (
    pd
    .merge(
        df
        .groupby(['fecha'], as_index=False)
        .agg(avg_oil_prod_bd_all=('oil_prod', 'mean')),
        df[df['nombre_pozo'].isin(y5_wells)]
        .groupby(['fecha'], as_index=False)
        .agg(avg_oil_prod_bd_y5=('oil_prod', 'mean')),
        how='left',
        on='fecha'
    )
)

# Save dataframe
OUTPUT_DIR = os.path.join("..", "..", "data", "processed")
os.makedirs(OUTPUT_DIR, exist_ok=True)
av_prod.to_csv(os.path.join(OUTPUT_DIR, "02_oil_production_per_month.csv"), sep=',', index=False)
