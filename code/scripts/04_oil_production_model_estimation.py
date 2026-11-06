#####################################################################
# 04 - OIL PRODUCTION MODEL ESTIMATION
# Author: Álvaro León G.
# Undergrad Thesis
# ITAM
#####################################################################
# Libraries
import pandas as pd
import os
from pathlib import Path
import statsmodels.api as sm

# Import regression dataframe
BASE_DIR = Path(__file__).resolve().parents[2]
DATA_PATH = BASE_DIR / "data" / "modeling"
df = (
    pd
    .read_csv(
        os.path.join(DATA_PATH, 'oil_production_regression_dataframe.csv'),
        parse_dates=['fecha'],
        date_format='%Y-%m-%d'
    )
)

# Get rid of the first two rows
df = df[df['fecha']>'2000-02-01'].copy()

# Define regressor columns
INDEP_VARS = [
    'd1_log_price',
    'l1_log_price',
    'd1_g',
    'l1_g',
    'time_effect'
]

# Create X (with and without time effects)
Xt = sm.add_constant(df[INDEP_VARS])
Xnt = sm.add_constant(df[INDEP_VARS][[c for c in INDEP_VARS if c not in ["time_effect"]]])

# Create Y
yt_all = df["d1_log_prod_all"]
yt_y5 = df["d1_log_prod_y5"]

# Model objects
model_01 = sm.OLS(yt_all, Xt)
model_02 = sm.OLS(yt_all, Xnt)
model_03 = sm.OLS(yt_y5, Xt)
model_04 = sm.OLS(yt_y5, Xnt)

# Estimation results
results_m01 = model_01.fit(cov_type='HAC',cov_kwds={'maxlags':4})
results_m02 = model_02.fit(cov_type='HAC',cov_kwds={'maxlags':4})
results_m03 = model_03.fit(cov_type='HAC',cov_kwds={'maxlags':4})
results_m04 = model_04.fit(cov_type='HAC',cov_kwds={'maxlags':4})

print(results_m01.summary())
print(results_m02.summary())
print(results_m03.summary())
print(results_m04.summary())
