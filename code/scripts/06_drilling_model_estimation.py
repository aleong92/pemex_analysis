#####################################################################
# 06 - MODEL ESTIMATION (DRILLING)
# Author: Álvaro León G.
# Undergrad Thesis
# ITAM
#####################################################################
# Libraries
import pandas as pd
import os
import statsmodels.api as sm

# Import production data
PATH = os.path.join('..', '..', 'data')
df_entry = pd.read_csv(PATH+'/regressions/oil_drill_regs_entry.csv', parse_dates=['fecha'], date_format='%Y-%m-%d')
df_op = pd.read_csv(PATH+'/regressions/oil_drill_regs_op.csv', parse_dates=['fecha'], date_format='%Y-%m-%d')

# One dataframe per information source (one for drilling, one for entry month) with non empty rows
df_entry = df_entry[df_entry['fecha']>'2000-03-01'].copy()
df_op = df_op[df_op['fecha']>'2002-03-01'].copy()

# Define regressor columns
INDEP_VARS = [
    'd1_log_price',
    'l1_log_price',
    'l2_log_price',
    'd1_g',
    'l1_g',
    'l2_g',
    'time_effect'
]

# Create X (with and without time effects) for both sources
Xt_entry = sm.add_constant(df_entry[INDEP_VARS])
Xnt_entry = sm.add_constant(df_entry[INDEP_VARS][[c for c in INDEP_VARS if c not in ["time_effect"]]])
Xt_op = sm.add_constant(df_op[INDEP_VARS])
Xnt_op = sm.add_constant(df_op[INDEP_VARS][[c for c in INDEP_VARS if c not in ["time_effect"]]])

# Create Y
yt_entry = df_entry["d1_log_wells_entry"]
yt_op = df_op["d1_log_wells_op"]

# Model objects
model_01 = sm.OLS(yt_entry, Xt_entry)
model_02 = sm.OLS(yt_entry, Xnt_entry)
model_03 = sm.OLS(yt_op, Xt_op)
model_04 = sm.OLS(yt_op, Xnt_op)

# Estimation results
results_m01 = model_01.fit(cov_type='HAC',cov_kwds={'maxlags':4})
results_m02 = model_02.fit(cov_type='HAC',cov_kwds={'maxlags':4})
results_m03 = model_03.fit(cov_type='HAC',cov_kwds={'maxlags':4})
results_m04 = model_04.fit(cov_type='HAC',cov_kwds={'maxlags':4})

print(results_m01.summary())
print(results_m02.summary())
print(results_m03.summary())
print(results_m04.summary())
