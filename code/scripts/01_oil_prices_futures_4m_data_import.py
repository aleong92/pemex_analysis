#####################################################################
# 01 - OIL PRODUCTION DATAFRAME
# Author: Álvaro León G.
# Undergrad Thesis
# ITAM
#####################################################################
# Libraries
import pandas as pd
import numpy as np
import os

# Define PATH and read West Texas Intermediate data
PATH = os.path.join('..', '..', 'data', 'prices', 'futures_4m.csv')
df = (
    pd.read_csv(
        filepath_or_buffer=PATH,
        header=None,
        skiprows=5,
        names=['f4m_price'],
        dtype={'f4m_price': np.float64}
    )
)

# Reset index
df.reset_index(drop=True, inplace=True)

# Invert month order
df['f4m_price'] = df['f4m_price'].iloc[::-1].values

# Create a month column
df['month'] = pd.date_range(start='1985-01-01', periods=len(df), freq='MS')

# Filter prices from 1999 to 2018
df = df.query("month > '1999-12-01' and month < '2019-01-01'")

# Save dataframe
df.to_csv(os.path.join("..", "..", "data", "prices_intermediate", "01_f4m_prices.csv"), sep=',', index=False)
