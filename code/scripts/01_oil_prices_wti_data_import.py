#####################################################################
# 01 - OIL PRICES DATA IMPORT PROCESS (WTI SPOT PRICES)
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
DATA_PATH = BASE_DIR / "data" / "raw" / "wti_spot.csv"
df = (
    pd
    .read_csv(
        filepath_or_buffer=DATA_PATH,
        header=None,
        skiprows=5,
        names=['wti_spot_price'],
        dtype={'wti_spot_price': np.float64}
    )
)

# Reset index
df.reset_index(drop=True, inplace=True)

# Invert month order
df['wti_spot_price'] = df['wti_spot_price'].iloc[::-1].values

# Create a month column
df['month'] = pd.date_range(start='1986-01-01', periods=len(df), freq='MS')

# Filter prices from 1999 to 2018
df = df.query("month > '1999-12-01' and month < '2019-01-01'")

# Save dataframe
OUTPUT_DIR = os.path.join("..", "..", "data", "intermediate")
os.makedirs(OUTPUT_DIR, exist_ok=True)
df.to_csv(os.path.join(OUTPUT_DIR, "01_wti_prices.csv"), sep=',', index=False)
