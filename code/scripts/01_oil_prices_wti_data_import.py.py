#####################################################################
# 01 - OIL PRODUCTION DATAFRAME
# Author: Álvaro León G.
# Undergrad Thesis
# ITAM
#####################################################################
# Libraries
import pandas as pd
import numpy as np
import datetime as dt
import glob
import re
import os
import sys

# Define PATH and read West Texas Intermediate data
PATH = os.path.join('..', '..', 'data', 'prices', 'wti_spot.csv')
df = (
    pd
    .read_csv(
        filepath_or_buffer=PATH,
        header=None,
        skiprows=5,
        names=['periodo', 'spot_precio_nominal'],
        dtype={'precio_nominal': np.float64}
    )
)
