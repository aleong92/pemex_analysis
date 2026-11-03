#####################################################################
# 04 - AVERAGE OIL PRODUCTION
# Author: Álvaro León G.
# Undergrad Thesis
# ITAM
#####################################################################
# Libraries
import pandas as pd
import os

# Import production data
PATH = os.path.join('..', '..', 'data', 'preexistent_wells', '03_preexistent_prod.csv')
df = (
    pd
    .read_csv(
        PATH,
        dtype={
            'nombre_pozo': str,
            'cuenca': str,
            'petroleo_mbd': float
        }
    )
)

# Parse date column
df['fecha'] = pd.to_datetime(df['fecha'], format='%Y-%m-%d')

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

# Compute mean well production for both sets of wells
AVG_PROD_PATH = os.path.join('..', '..', 'data', 'average_production')
av_prod_all_wells = (
    df
    .groupby(['fecha'], as_index=False)
    .agg(avg_oil_prod_bd=('oil_prod', 'mean'))
    .to_csv(AVG_PROD_PATH+'/avg_oil_prod_all_wells.csv', sep=',', index=False)
)
av_prod_y5_wells = (
    df[df['nombre_pozo'].isin(y5_wells)]
    .groupby(['fecha'], as_index=False)
    .agg(avg_oil_prod_bd=('oil_prod', 'mean'))
    .to_csv(AVG_PROD_PATH+'/avg_oil_prod_y5_wells.csv', sep=',', index=False)
)
