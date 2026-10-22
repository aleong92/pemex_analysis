#####################################################################
# 04 - AGGREGATE WELL DRILLING
# Author: Álvaro León G.
# Undergrad Thesis
# ITAM
#####################################################################
# Libraries
import pandas as pd
import numpy as np
import os

# Import production data
PATH = os.path.join('..', '..', 'data')
df_op = pd.read_csv(PATH+'/oil_intermediate/02_drill_op.csv')
df_entry = pd.read_csv(PATH+'/oil_intermediate/02_well_inventory.csv').rename(columns={'production_start':'fecha'})
df_prices = pd.read_csv(PATH+'/prices_final/02_oil_prices.csv')[['month', 'spot_price_201812_usd', 'f4m_price_201812_usd']].rename(columns={'month':'fecha'})

# Set date format for date columns
df_op['fecha'] = pd.to_datetime(df_op['fecha'], format='%Y-%m-%d')
df_entry['fecha'] = pd.to_datetime(df_entry['fecha'], format='%Y-%m-%d')
df_prices['fecha'] = pd.to_datetime(df_prices['fecha'], format='%Y-%m-%d')

# Aggregate drilling by month in both dataframes and merge with prices
df_agg = (
    pd
    .merge(
        df_entry[(df_entry['fecha'].dt.year>1999) & (df_entry['fecha'].dt.year<2019)].groupby(['fecha'], as_index=False).agg(n_wells_entry = ('nombre_pozo', 'count')),
        df_op.groupby(['fecha'], as_index=False).agg(n_wells_op = ('pozos_perforados', 'sum')),
        how='left',
        on='fecha'
    )
    .merge(
        df_prices,
        how='inner',
        on='fecha',
        validate='1:1'
    )
)

# Estimate percentage difference between 4-month futures and spot prices
df_agg['g_diff'] = ((df_agg['f4m_price_201812_usd'] / df_agg['spot_price_201812_usd']) - 1) * 100

# Estimate logarithms
df_agg['log_wells_entry'] = np.log(df_agg['n_wells_entry'])
df_agg['log_wells_op'] = np.log(df_agg['n_wells_op'])
df_agg['log_price'] = np.log(df_agg['spot_price_201812_usd'])

# Estimate first differences
df_agg['d1_log_wells_entry'] = df_agg['log_wells_entry'] - df_agg['log_wells_entry'].shift(periods=1)
df_agg['d1_log_wells_op'] = df_agg['log_wells_op'] - df_agg['log_wells_op'].shift(periods=1)
df_agg['d1_log_price'] = df_agg['log_price'] - df_agg['log_price'].shift(periods=1)
df_agg['d1_g'] = df_agg['g_diff'] - df_agg['g_diff'].shift(periods=1)

# Lagged first differences
df_agg['l1_log_price'] = df_agg['d1_log_price'].shift(periods=1)
df_agg['l2_log_price'] = df_agg['d1_log_price'].shift(periods=2)
df_agg['l1_g'] = df_agg['d1_g'].shift(periods=1)
df_agg['l2_g'] = df_agg['d1_g'].shift(periods=2)

# Time factor
df_agg['time_effect'] = ((pd.to_datetime(df_agg['fecha'], format='%Y-%m-%d').dt.year) - 2000) + 1

# Save into csv file
REG_COLUMNS = [
    'd1_log_wells_entry',
    'd1_log_wells_op',
    'l1_log_price',
    'l2_log_price',
    'l1_g',
    'l2_g',
    'time_effect'
]
df_agg[REG_COLUMNS].to_csv(PATH+'/regressions/oil_drill_regs.csv', sep=',', index=False)
