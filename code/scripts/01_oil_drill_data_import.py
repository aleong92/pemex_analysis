#####################################################################
# 01 - OIL DRILLING DATAFRAME
# Author: Álvaro León G.
# Undergrad Thesis
# ITAM
#####################################################################
# Libraries
import pandas as pd
import glob
import os
import sys

# Append config to system path and import SIH dictionaries
sys.path.append(os.path.abspath(os.path.join("..", "..")))
from config.config import CNH_MAP_DTYPES, CNH_MAP_NAMES

# Define PATH and get file names in the folder
PATH = os.path.join('..', '..', 'data', 'oil_drilling')
PERF_FILENAMES = [i for i in glob.glob(PATH+'/drill_*.{}'.format('csv'))]

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

# Initial well count
print(f"""
      OIL WELLS DATABASE
      ------------------

      Wells:      {df['nombre_pozo'].nunique():>7,}

""")

# Save dataframe
df.to_csv(os.path.join("..", "..", "data", "oil_intermediate", "01_oil_drill.csv"), sep=',', index=False)
