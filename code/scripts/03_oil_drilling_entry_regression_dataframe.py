#####################################################################
# 03 - OIL DRILLING (ENTRY) REGRESSIONS
# Author: Álvaro León G.
# Undergrad Thesis
# ITAM
#####################################################################
# Libraries
import pandas as pd
import numpy as np
import os
from pathlib import Path

# Import drilling by entry month
BASE_DIR = Path(__file__).resolve().parents[2]
DATA_PATH = BASE_DIR / "data" / "processed"
df = (
    pd
    .read_csv(
        os.path.join(DATA_PATH, '02_oil_drilling_entry.csv'),
        parse_dates=['fecha'],
        date_format='%Y-%m-%d'
    )
    .merge(
        pd.read_csv(
            os.path.join(DATA_PATH, '02_oil_prices.csv'),
            parse_dates=['month'],
            date_format='%Y-%m-%d'
        )
        .rename(columns={'month':'fecha'}),
        how='inner',
        on='fecha',
        validate='1:1'
    )
)

# Estimate percentage difference between 4-month futures and spot prices
df['g_diff'] = ((df['f4m_price_201812_usd'] / df['spot_price_201812_usd']) - 1) * 100

# Estimate logarithms
df['log_wells_entry'] = np.log(df['n_wells_entry'])
df['log_price'] = np.log(df['spot_price_201812_usd'])

# Estimate first differences
df['d1_log_wells_entry'] = df['log_wells_entry'] - df['log_wells_entry'].shift(periods=1)
df['d1_log_price'] = df['log_price'] - df['log_price'].shift(periods=1)
df['d1_g'] = df['g_diff'] - df['g_diff'].shift(periods=1)

# Lagged first differences
df['l1_log_price'] = df['d1_log_price'].shift(periods=1)
df['l2_log_price'] = df['d1_log_price'].shift(periods=2)
df['l1_g'] = df['d1_g'].shift(periods=1)
df['l2_g'] = df['d1_g'].shift(periods=2)

# Time factor
df['time_effect'] = ((pd.to_datetime(df['fecha'], format='%Y-%m-%d').dt.year) - 2000) + 1

# Save into csv file
REG_COLUMNS = [
    'fecha',
    'd1_log_wells_entry',
    'd1_log_price',
    'l1_log_price',
    'l2_log_price',
    'd1_g',
    'l1_g',
    'l2_g',
    'time_effect'
]
OUTPUT_DIR = os.path.join("..", "..", "data", "modeling")
os.makedirs(OUTPUT_DIR, exist_ok=True)
df[REG_COLUMNS].to_csv(os.path.join(OUTPUT_DIR,'oil_drilling_entry_regression_dataframe.csv'), sep=',', index=False)
