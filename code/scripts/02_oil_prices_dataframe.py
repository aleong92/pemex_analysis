#####################################################################
# 02 - OIL PRICES DATAFRAME
# Author: Álvaro León G.
# Undergrad Thesis
# ITAM
#####################################################################
# Libraries
import pandas as pd
import os
from pathlib import Path

# Consolidate price data in single dataframe
BASE_DIR = Path(__file__).resolve().parents[2]
DATA_PATH = BASE_DIR / "data" / "intermediate"
df = (
    pd
    .merge(
        pd.read_csv(os.path.join(DATA_PATH, '01_wti_prices.csv')),
        pd.read_csv(os.path.join(DATA_PATH, '01_f4m_prices.csv')),
        how='inner',
        on='month',
        validate='1:1'
    )
    .merge(
        pd.read_csv(os.path.join(DATA_PATH, '01_cpi_index.csv')),
        how='inner',
        on='month',
        validate='1:1'
    )
)

# Create a spot price column for spot and future prices
df['spot_price_201812_usd'] = (df['wti_spot_price'] / df['cpi_base_201812']) * 100
df['f4m_price_201812_usd'] = (df['f4m_price'] / df['cpi_base_201812']) * 100

# Save dataframe
OUTPUT_DIR = os.path.join("..", "..", "data", "processed")
os.makedirs(OUTPUT_DIR, exist_ok=True)
df.to_csv(os.path.join(OUTPUT_DIR, "02_oil_prices.csv"), sep=',', index=False)
