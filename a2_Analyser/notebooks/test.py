#% pip install openpyxl
import os, re, configparser
import pandas as pd
import numpy as np
from globals import glob
from utilities_database import prepare_data, prepare_database, consult_database, clear_databases, retrieve_data, rename_index, get_date, get_sigma, rename_limits_table
from utilities_analysis import mean_calculator, limits_generator, ini_generator_personalized, RyR, z_score_filter, reset_df
from utilities_plotting import plot_scatter
import _db_tools as db
import pandas as pd
from globals import glob
import matplotlib.pyplot as plt

#Data extraction
table_names = ['TOP_PASSAT_B9_measurements_2023y_11m_14d_17h_21m_03s', 'TOP_PASSAT_B9_limits_2023y_11m_14d_17h_21m_03s']
MEAS = retrieve_data("input.db", table_names[0])
LIMITS = retrieve_data("input.db", table_names[1])
print(MEAS)

#Data preparation
MEAS_format = rename_index(MEAS)
new_column_names = {old_col: f"test: {i+1}" for i, old_col in enumerate(MEAS_format.columns)}
MEAS_format.rename(columns=new_column_names, inplace=True)
print("Measurements:")
MEAS_format #Shows the df in html format

LIMITS_format = rename_index(LIMITS)
LIMITS_format.columns = ['LO_LIMIT', 'HI_LIMIT']
print("limits:")
LIMITS_format

def plot_scatter(MEAS_format, LIMITS_format, label, sigma):
    ''''Plot a scatter plot with the values of a single fiber'''
    row = MEAS_format.loc[label]
    plt.scatter(range(1, len(row) + 1), row.values, color='blue', alpha=0.7, label='Measured Values')
    try:
        low_limit = LIMITS_format.loc[label]['LO_LIMIT']
        high_limit = LIMITS_format.loc[label]['HI_LIMIT']
    except:
        low_limit = LIMITS_format.loc[label]['LSL']
        high_limit = LIMITS_format.loc[label]['USL']
    plt.axhline(low_limit, color='red', linestyle='dashed', linewidth=2, label=f"Low Specification Level: {round(low_limit, 4)}")
    plt.axhline(high_limit, color='red', linestyle='dashed', linewidth=2, label=f"High Specification Level: {round(high_limit, 4)}")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xlabel('Measurement Index')
    plt.ylabel('Values')
    plt.title(f'Values for: {label} (Sigma: {sigma})')
    plt.show()

# Test the function
fiber_label = 'Fiber_1'
sigma_value = 1.5
plot_scatter(MEAS_format, LIMITS_format, fiber_label, sigma_value)
