#####################################################################
# 01 - OIL PRICES DATA IMPORT PROCESS (CPI INDEX)
# Author: Álvaro León G.
# Undergrad Thesis
# ITAM
#####################################################################
# Libraries
import pandas as pd
import numpy as np
import os
from pathlib import Path

# Define PATH and read West Texas Intermediate data
BASE_DIR = Path(__file__).resolve().parents[2]
DATA_PATH = BASE_DIR / "data" / "raw" / "cpi.csv"
PATH = os.path.join('..', '..', 'data', 'prices', 'cpi.csv')
df = (
    pd.read_csv(
        filepath_or_buffer=DATA_PATH,
        header=None,
        skiprows=1,
        names=['series_id', 'año', 'period', 'cpi_base_og'],
        dtype={'cpi_baseog': np.float64}
    )
)

# Get rid of non-monthly observations
df = df[~(df['period'].str.contains("S"))].copy()

# Create a month column
df['month'] = pd.date_range(start='1995-01-01', periods=len(df), freq='MS')

# Filter prices from 1999 to 2018
df = df.query("month > '1999-12-01' and month < '2019-01-01'")

# Change the base to Dec-2018
NEW_BASE = df.loc[df['month'] == '2018-12-01', 'cpi_base_og'].values[0]
df['cpi_base_201812'] = (df['cpi_base_og'] * 100) / NEW_BASE

# Save dataframe
OUTPUT_DIR = os.path.join("..", "..", "data", "intermediate")
os.makedirs(OUTPUT_DIR, exist_ok=True)
(
    df[['month', 'cpi_base_og', 'cpi_base_201812']]
    .to_csv(os.path.join(OUTPUT_DIR, "01_cpi_index.csv"), sep=',', index=False)
)
