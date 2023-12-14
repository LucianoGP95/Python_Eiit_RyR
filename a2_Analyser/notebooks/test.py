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

os.chdir(os.path.dirname(os.path.realpath(__file__)))  ####Delete after debugging

def ini_generator(limits: pd.DataFrame, lenses_per_nest: int) -> None:
    '''Generates an ini file with personalized limits for every mean.
    Parameters:
    - limits (pd.DataFrame): DataFrame containing the personalized limits for each mean.
        The DataFrame is expected to have two columns, where the first column represents
        the lower limit and the second column represents the upper limit.
    - lenses_per_nest (int): Number of lenses per nest. Should be 3 or 4.
    Raises:
    ValueError: If lenses_per_nest is neither 3 nor 4.
    The function reads a template .ini file based on the lenses_per_nest parameter,
    updates the limits in the template with the provided limits DataFrame, and
    saves the modified data to a new .ini file.
    Example:
    >>> import pandas as pd
    >>> limits_data = {'LO_LIMIT': [10, 15, 20], 'HI_LIMIT': [30, 35, 40]}
    >>> limits_df = pd.DataFrame(limits_data)
    >>> ini_generator(limits_df, 3)
    '''
    class CaseSensitiveConfigParser(configparser.ConfigParser):
        '''
        A custom class to override optionxform and avoid uppercases being converted to lowercases.
        '''
        def optionxform(self, optionstr):
            return optionstr
    config = CaseSensitiveConfigParser()
    #Import a template based on the number of lenses per nest
    if lenses_per_nest == 3:
        config.read('../data/template_12_fibers.ini')
    elif lenses_per_nest == 4:
        config.read('../data/template_16_fibers.ini')
    else:
        raise ValueError("lenses_per_nest should be 3 or 4.")
    keys_list = []
    #Get a keys list with the correct uppercased keys
    for section_name in config.sections():
        section = config[section_name]
        keys_list.extend(section.keys())
    HI_LIMIT = limits.iloc[:, 1]
    LO_LIMIT = limits.iloc[:, 0]
    #Iterate through the sections and options in the .ini file
    for section in config.sections():
        keys_list = list(config[section].keys())
        j = 0
        for i in range(0, len(keys_list), 2):
            key1 = keys_list[i]
            key2 = keys_list[i + 1]
            col1 = str(limits.iloc[j, 1])
            col2 = str(limits.iloc[j, 0])
            j += 1
            config[section][key1] = col1
            config[section][key2] = col2
    #Print the five first elements of the .ini for a quick check
    for section in config.sections():
        print(f"[{section}]")
        i = 0
        for key, value in config.items(section):
            if i < 5:
                print(f"{key} = {value}")
                i += 1
            else:
                break
        print("...")
    #Save the modified data to a new .ini file
    save_path = os.path.abspath(f'../a2_output/{glob.tooling}.ini')
    with open(save_path, 'w') as configfile:
        for section in config.sections():
            configfile.write(f"[{section}]\n")
            keys = keys_list  #Recover the original keys to write them in the .ini file
            for i, key in enumerate(keys):
                configfile.write(f"{key} = {config[section][key]}\n")
                if (i + 1) % 4 == 0 and i < len(keys) - 1:  #Insert a blank line every four keys
                    configfile.write("\n")

limits_data = {'LO_LIMIT': [10, 15, 20], 'HI_LIMIT': [30, 35, 40]}
limits_df = pd.DataFrame(limits_data)
ini_generator(limits_df, 3)
