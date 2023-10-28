import pandas as pd
import os
from globals import glob
from utilities import prepare_database
import configparser
import sys
sys.path.append("../tools/")
import _db_tools as db #Personal tool for managing sqlite databases in data science

####Helper Functions####
def mean_calculator(measures: pd.DataFrame, lenses_per_nest=None) -> list[float]:
    '''Calculate the desired means:
    Parameters:
    - measures (DataFrame): The input DataFrame containing fiber measurements.
    - lenses_per_nest (int, optional): The number of lenses per nest for specific means calculation. If None, global means are calculated.
    - Returns:
    list: A list containing the mean values for fbx and fby. If lenses_per_nest is specified, it returns specific means for each position.
    If lenses_per_nest is None:
    - Calculates a global mean for fbx and fby.
    - Returns the mean values for both fbx and fby in a list.
    - Displays the mean values for fbx and fby.
    If lenses_per_nest is specified:
    - Calculates specific means for each position for fbx and fby based on the number of lenses per nest.
    - Returns a list containing specific mean values for fbx and fby for each position.
    - Displays the specific mean values for fbx and fby per position.'''
    resume = measures.transpose().describe() #Transpose the df first due to describe() working in columns.
    rough_means = list(resume.iloc[1, :].values)
    means = []; means_fbx = []; means_fby = [] #Preallocation
    if lenses_per_nest == None: #Calculates a global mean for fbx and for fby
        for i, mean in enumerate(rough_means): #Iterates and rounds every mean value
            mean = round(mean, 4)
            means_fbx.append(mean) if i % 2 == 0 else means_fby.append(mean)
            means.append(mean)
        abs_mean_fbx = sum(means_fbx) / len(means_fbx)
        abs_mean_fby = sum(means_fby) / len(means_fby)
        means = [abs_mean_fbx, abs_mean_fby]
        print("Means (fbx and fby):") 
        print("Fiber x: " + str(round(abs_mean_fbx, 4)))
        print("Fiber y: " + str(round(abs_mean_fby, 4)))
    else: #Calculates specific means for each position for fbx and fby
        for index in range(lenses_per_nest*2):
            if index % 2 == 0:
                mean_fbx = rough_means[0::2] #Gets fbx values
                mean_fbx = mean_fbx[index::lenses_per_nest] #Gets the values of the specific lens
                abs_mean_fbx = sum(mean_fbx) / len(mean_fbx)
                means_fbx.append(abs_mean_fbx)
            else:
                mean_fby = rough_means[0::2] #Gets fby values
                mean_fby = mean_fby[index::lenses_per_nest] #Gets the values of the specific lens
                abs_mean_fby = sum(mean_fby) / len(mean_fby)
                means_fby.append(abs_mean_fby)
        means = means_fbx + means_fby
        print("Means per position (from lower to higher):") 
        print("  Fiber x: ")
        print([round(value, 4) for value in means_fbx])
        print("  Fiber y: ")
        print([round(value, 4) for value in means_fby])
    return means

def limits_gen(measures: pd.DataFrame, means: list, lenses_per_nest = None) -> pd.DataFrame:
    '''Generate the limit values for a list containing the means in a DataFrame.
    Calculates the total mean for each fiber axis and applies it to the corresponding rows.
    Parameters:
    - measures (pd.DataFrame): The measures dataframe to get its size.
    - means (list): A list of means to generate limits for.
    Returns:
    - limits: A dataframe containing the generated limits.'''
    x_tolerance = glob.x_tolerance
    y_tolerance = glob.y_tolerance
    limits = pd.DataFrame(columns=["LO_LIMIT", "HI_LIMIT"]) #Columns names
    if lenses_per_nest == None: #Calculates a global mean for fbx and for fby
        for index in range(int(measures.shape[0] / (lenses_per_nest * 2))): #Iterates over the positions of the dataframe
            if index % 2 == 0: #Fbx rows
                low_limit = round(means[0] - x_tolerance, 4)
                high_limit = round(means[0] + x_tolerance, 4)
            else: #Fby rows
                low_limit = round(means[1] - y_tolerance, 4)
                high_limit = round(means[1] + y_tolerance, 4)
            current_limits_df = pd.DataFrame({"LO_LIMIT": [low_limit], "HI_LIMIT": [high_limit]}) #Create a DataFrame with the current low_limit and high_limit values
            limits = pd.concat([limits, current_limits_df], ignore_index=True, axis=0) #Concatenate the current limits DataFrame with the main 'limits' DataFrame
    else: #Calculates specific limits per each position for fbx and fby
        new_order = [0, 3, 1, 4, 2, 5]
        ordered_means = [means[i] for i in new_order]
        for _ in range(int(measures.shape[0] / (lenses_per_nest * 2))):  # Iterates over every position (e.g. 24/6=4 positions)
            for j in range(len(ordered_means)):
                if j % 2 == 0:
                    low_limit = round(ordered_means[j] - x_tolerance, 4)
                    high_limit = round(ordered_means[j] + x_tolerance, 4)
                else:
                    low_limit = round(ordered_means[j] - y_tolerance, 4)
                    high_limit = round(ordered_means[j] + y_tolerance, 4)
                current_limits_df = pd.DataFrame({"LO_LIMIT": [low_limit], "HI_LIMIT": [high_limit]}) 
                limits = pd.concat([limits, current_limits_df], ignore_index=True, axis=0) 
    return limits

def ini_generator_personalized(limits: pd.DataFrame) -> None:
    '''Generates a ini file with personalized limits for every mean'''
    class CaseSensitiveConfigParser(configparser.ConfigParser):
        '''A custom class to override optionxform and avoid uppercases being converted to lowercase
        It just works F76 F76 F76 F76 F76'''
        def optionxform(self, optionstr):
            return optionstr
    config = CaseSensitiveConfigParser()
    config.read('../data/template.ini') #Import a template
    keys_list = []
    for section_name in config.sections(): #Get a keys list with the correct uppercased keys
        section = config[section_name]
        keys_list.extend(section.keys())
    HI_LIMIT = limits.iloc[:, 1]
    LO_LIMIT = limits.iloc[:, 0]
    for section in config.sections(): #Iterate through the sections and options in the .ini file
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
    for section in config.sections(): #Print the five first elements of the .ini for a quick check
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
    with open(f'../a2_output/{glob.tooling}.ini', 'w') as configfile:
        for section in config.sections():
            configfile.write(f"[{section}]\n")
            keys = keys_list #Recover the original keys to write them in the .ini file
            for i, key in enumerate(keys):
                configfile.write(f"{key} = {config[section][key]}\n")
                if (i + 1) % 4 == 0 and i < len(keys) - 1: #Insert a blank line every four keys
                    configfile.write("\n")

#Data preparation
dbh = db.SQLite_Data_Extractor("database.db") #Connect to the database
measures = dbh.retrieve(glob.tooling) #Get the desired tooling data
dbh.close_conn() 

means = mean_calculator(measures, glob.lenses_per_nest)

limits = limits_gen(measures, means, glob.lenses_per_nest)
limits

means = [10, 20, 30, 40, 50, 60]
new_order = [0, 3, 1, 4, 2, 5]
ordered_means = [means[i] for i in new_order]
print(ordered_means)

