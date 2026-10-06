#####################################################################
# 03 - OIL DRILLING BY OPERATOR
# Author: Álvaro León G.
# Undergrad Thesis
# ITAM
#####################################################################
# Libraries
import pandas as pd
import os
import sys

# Append config to system path and import OP dictionaries
sys.path.append(os.path.abspath(os.path.join("..", "..")))
from config.config import OP_BASIN, OP_LOCATION, OP_WELL_CAT

# Import drilling data
PATH = os.path.join('..', '..', 'data', 'oil_drilling')
df_op = (
    pd
    .read_csv(
        PATH+'/pozos_operador.csv',
        encoding='latin-1',
        skiprows=6,
        header=None,
        names=['mes_año', 'cuenca', 'categoria', 'ubicacion', 'operador', 'pozos_perforados']
    )
)

# Parse and format date column
df_op['fecha'] = (
    df_op['mes_año'].str.split('/').str[1]+'-'+
    df_op['mes_año'].str.split('/').str[0]+'-01'
)
df_op['fecha'] = pd.to_datetime(df_op['fecha'], format='%Y-%m-%d')

# Filter by date and operator
df_op = df_op[df_op['fecha'].dt.year < 2019].copy()
df_op = df_op[df_op['operador'] == 'Pemex Exploración y Producción'].copy()

# Drop duplicate rows
df_op.drop_duplicates(subset=['fecha','cuenca', 'categoria', 'ubicacion'], keep='first', inplace=True)

# Map OP dictionaries
df_op['cuenca'] = df_op['cuenca'].map(OP_BASIN)
df_op['ubicacion'] = df_op['ubicacion'].map(OP_LOCATION)
df_op['categoria'] = df_op['categoria'].map(OP_WELL_CAT)

# Write to csv
(
    df_op[['fecha', 'cuenca', 'ubicacion', 'categoria', 'pozos_perforados']]
    .to_csv(os.path.join('..', '..', 'data', 'oil_intermediate', '02_drill_op.csv'), sep=',', index=False))
