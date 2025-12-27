#####################################################################
# 02 - OIL PRICES DATAFRAME
# Author: Álvaro León G.
# Undergrad Thesis
# ITAM
#####################################################################
# Libraries
import pandas as pd
import numpy as np
import os

# Import price and cpi data and consolidate in single dataframe
PATH = os.path.join('..', '..', 'data', 'prices_intermediate')
df = (
    pd
    .merge(
        pd.read_csv(PATH+'/01_wti_prices.csv'),
        pd.read_csv(PATH+'/01_f4m_prices.csv'),
        how='inner',
        on='month',
        validate='1:1'
    )
    .merge(
        pd.read_csv(PATH+'/01_cpi_index.csv'),
        how='inner',
        on='month',
        validate='1:1'
    )
)

# Save dataframe
df.to_csv(os.path.join("..", "..", "data", "prices_final", "02_oil_prices.csv"), sep=',', index=False)
