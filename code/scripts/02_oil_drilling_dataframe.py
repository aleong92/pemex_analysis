#####################################################################
# 02 - AGGREGATE WELL DRILLING
# Author: Álvaro León G.
# Undergrad Thesis
# ITAM
#####################################################################
# Libraries
import pandas as pd
import os
from pathlib import Path

# Import drilling intermediate data
BASE_DIR = Path(__file__).resolve().parents[2]
DATA_PATH = BASE_DIR / "data" / "intermediate"
df_op = pd.read_csv(
    os.path.join(DATA_PATH, '01_oil_op.csv'),
    parse_dates=['fecha'],
    date_format='%Y-%m-%d'
)
df_drill = (
    pd
    .read_csv(
        os.path.join(DATA_PATH, '01_well_inventory.csv'),
        parse_dates=['production_start'],
        date_format='%Y-%m-%d'
    )
    .rename(columns={'production_start':'fecha'})
)

# Aggregate drilling by month
df_op_agg = (
    df_op
    .groupby(['fecha'], as_index=False)
    .agg(n_wells_op = ('pozos_perforados', 'sum'))
)
df_drill_agg = (
    df_drill[(df_drill['fecha'].dt.year>1999) & (df_drill['fecha'].dt.year<2019)]
    .groupby(['fecha'], as_index=False)
    .agg(n_wells_entry = ('nombre_pozo', 'count'))
)

# Save dataframe
OUTPUT_DIR = os.path.join("..", "..", "data", "processed")
os.makedirs(OUTPUT_DIR, exist_ok=True)
df_drill_agg.to_csv(os.path.join(OUTPUT_DIR, "02_oil_drilling_entry.csv"), sep=',', index=False)
df_op_agg.to_csv(os.path.join(OUTPUT_DIR, "02_oil_drilling_operator.csv"), sep=',', index=False)
