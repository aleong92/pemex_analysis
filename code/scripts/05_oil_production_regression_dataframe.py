#####################################################################
# 05 - OIL PRODUCTION REGRESSIONS
# Author: Álvaro León G.
# Undergrad Thesis
# ITAM
#####################################################################
# Libraries
import pandas as pd
import numpy as np
import os

# Import average production from preexistent wells and price data
PATH = os.path.join('..', '..', 'data')
df_reg = (
    pd
    .merge(
        pd.read_csv(PATH+'/average_production/avg_oil_prod_all_wells.csv'),
        pd.read_csv(PATH+'/average_production/avg_oil_prod_y5_wells.csv'),
        how='inner',
        on='fecha',
        suffixes=('_all', '_y5'),
        validate='1:1'
    )
    .merge(
        pd.read_csv(PATH+'/prices_final/02_oil_prices.csv')[['month', 'spot_price_201812_usd', 'f4m_price_201812_usd']]
        .rename(columns={'month':'fecha'}),
        how='inner',
        on='fecha',
        validate='1:1'
    )
)

# Estimate percentage difference between 4-month futures and spot prices
df_reg['g_diff'] = ((df_reg['f4m_price_201812_usd'] / df_reg['spot_price_201812_usd']) - 1) * 100

# Estimate logarithms
df_reg['log_prod_all'] = np.log(df_reg['avg_oil_prod_bd_all'])
df_reg['log_prod_y5'] = np.log(df_reg['avg_oil_prod_bd_y5'])
df_reg['log_price'] = np.log(df_reg['spot_price_201812_usd'])

# Estimate first differences
df_reg['d1_log_prod_all'] = df_reg['log_prod_all'] - df_reg['log_prod_all'].shift(periods=1)
df_reg['d1_log_prod_y5'] = df_reg['log_prod_y5'] - df_reg['log_prod_y5'].shift(periods=1)
df_reg['d1_log_price'] = df_reg['log_price'] - df_reg['log_price'].shift(periods=1)
df_reg['d1_g'] = df_reg['g_diff'] - df_reg['g_diff'].shift(periods=1)

# Lagged first differences
df_reg['l1_log_price'] = df_reg['d1_log_price'].shift(periods=1)
df_reg['l1_g'] = df_reg['d1_g'].shift(periods=1)

# Time factor
df_reg['time_effect'] = ((pd.to_datetime(df_reg['fecha'], format='%Y-%m-%d').dt.year) - 2000) + 1

# Save into csv file
REG_COLUMNS = [
    'd1_log_prod_all',
    'd1_log_prod_y5',
    'd1_log_price',
    'l1_log_price',
    'd1_g',
    'l1_g',
    'time_effect'
]
df_reg[REG_COLUMNS].to_csv(PATH+'/regressions/oil_prod_regs.csv', sep=',', index=False)
