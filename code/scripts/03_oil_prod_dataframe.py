#####################################################################
# 03 - OIL PRODUCTION DATAFRAME
# Author: Álvaro León G.
# Undergrad Thesis
# ITAM
#####################################################################
# Libraries
import pandas as pd
import os

# Import production data
PATH = os.path.join('..', '..', 'data', 'oil_intermediate')
df = (
    pd
    .read_csv(
        PATH+'/01_oil_prod.csv',
        usecols=['fecha', 'cuenca', 'nombre_pozo', 'petroleo_mbd']
    )
)

# List of identified oil wells
inv = (
    pd
    .read_csv(
        PATH+'/02_well_inventory.csv',
        usecols=['nombre_pozo', 'production_start', 'preexistent_well']
    )
)
PREEX_WELLS = inv[inv['preexistent_well'] == 1]['nombre_pozo'].unique().tolist()

# Filter production from oil wells
df = df[df['nombre_pozo'].isin(PREEX_WELLS)].copy()

# Observations from 2000 to 2018
df = df.query("fecha > '1999-12-01' and fecha < '2019-01-01'")

# Save dataframe
df.to_csv(os.path.join("..", "..", "data", "preexistent_wells", "03_preexistent_prod.csv"), sep=',', index=False)
