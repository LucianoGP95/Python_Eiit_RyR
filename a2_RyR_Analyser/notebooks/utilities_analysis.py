import pandas as pd
import numpy as np
from globals import glob
import configparser
import matplotlib.pyplot as plt

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

def limits_gen(measurements: pd.DataFrame, means: list, lenses_per_nest=None) -> pd.DataFrame:
    '''Generate the limit values for a list containing the means in a DataFrame.
    Calculates the total mean for each fiber axis and applies it to the corresponding rows.
    Parameters:
    - measures (pd.DataFrame): The measurements dataframe to get its size.
    - means (list): A list of means to generate limits for.
    - lenses_per_nest (int, optional): The number of lenses per nest for specific means calculation. If None, global means are calculated.
    Returns:
    - limits: A dataframe containing the generated limits.'''
    x_tolerance = glob.x_tolerance
    y_tolerance = glob.y_tolerance
    limits = pd.DataFrame(columns=["LO_LIMIT", "HI_LIMIT"]) #Columns names
    if lenses_per_nest == None: #Calculates a global mean for fbx and for fby
        for index in range(int(measurements.shape[0] / (lenses_per_nest * 2))): #Iterates over the positions of the dataframe
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
        ordered_means = [means[i] for i in new_order] #Reorder de the means for implementation
        for _ in range(int(measurements.shape[0] / (lenses_per_nest * 2))):  # Iterates over every nest (e.g. 24/6=4 nests)
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

def RyR(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate the RyR values for both fibers and provide a qualitative evaluation for each value.
    Parameters:
    - df (pd.DataFrame): The input DataFrame containing fiber measurements
    Returns:
    pd.DataFrame: A DataFrame containing the RyR values and qualitative evaluation for both fibers.
    The DataFrame includes the RyR values and a qualitative evaluation for each value."""
    #df = df.iloc[:, 1:]
    std = df.iloc[:, :-2].std(axis=1)  # Standard deviation for each row, excluding limits
    df_RyR = (6 * std / (df.iloc[:, -1] - df.iloc[:, -2])) * 100  # Calculate RyR for the whole DataFrame
    df_RyR = pd.DataFrame(df_RyR, columns=['RyR'])  # Build a new DataFrame with the RyR values
    pass_df = qualitative_evaluation(df_RyR)  # Qualitative evaluation for RyR values
    RyR = pd.concat([df_RyR, pass_df], axis=1)
    return RyR

def qualitative_evaluation(df: pd.DataFrame) -> pd.DataFrame:
    """Provide a qualitative evaluation for each RyR value in a DataFrame.
    Parameters:
    - df (pd.DataFrame): The input DataFrame containing RyR values for a fiber.
    Returns:
    pd.DataFrame: A DataFrame containing the qualitative evaluation for the input fiber.
    The DataFrame includes a qualitative evaluation ('Status') for each RyR value."""
    pass_df = pd.DataFrame()
    for _, ryr_value in enumerate(df['RyR']):
        status = "Correct" if ryr_value <= 10 else ("Low fail" if 10 < ryr_value <= 25 else "High fail")
        pass_df = pd.concat([pass_df, pd.DataFrame([status], columns=['Status'])], axis=0)
    pass_df.reset_index(drop=True, inplace=True)
    return pass_df

def z_score_filter(df: pd.DataFrame, threshold=1) -> pd.DataFrame:
    """Applies a z-score filter to a DataFrame, removing values that do not meet the specified threshold.
    Parameters:
    - df (pd.DataFrame): The input DataFrame containing the measurements and limits.
    - threshold (float): The z-score threshold. Values exceeding this threshold will be replaced with NaN.
    Returns:
    pd.DataFrame: A new DataFrame with values that pass the z-score filter, while retaining the original limits columns.
    For each row in the input DataFrame, the function calculates the z-scores for the measurement values and
    replaces values with z-scores greater than the specified threshold with NaN. The original limits columns are retained."""
    rows = []
    measures = df.iloc[:, :-2]  #Indexes the measurements
    limits = df.iloc[:, -2:]  #Indexes the limits
    for row_idx in range(measures.shape[0]):  # Iterates over the rows
        row = measures.iloc[row_idx, :]
        if row.std() == 0: #If the standard deviation is zero, don't calculate z-scores and keep the original values
            filtered_row = row
        else:
            z_scores = (row - row.mean()) / row.std()  #Calculates the z-score
            filtered_row = np.where(abs(z_scores) <= threshold, row, np.nan)  #Applies the threshold as a filter
        rows.append(filtered_row)
    filtered_df = pd.DataFrame(rows)  #Builds a new DataFrame
    filtered_df = pd.concat([filtered_df, limits], axis=1)  #Adds back the columns
    return filtered_df

#Test script
if __name__ == '__main__':
    df = pd.read_excel(r"C:\Users\luciano.galan\Desktop\Code\Python_Eiit_RyR\a2_RyR_Analyser\a2_output\TOP_Passat_B9_2023y-11m-16d_11h-10m-21s.xlsx")
    RyRdf = RyR(df)
    RyRdf