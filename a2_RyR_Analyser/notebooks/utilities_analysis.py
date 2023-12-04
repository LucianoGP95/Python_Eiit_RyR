import pandas as pd
import numpy as np
from globals import glob
import configparser
import matplotlib.pyplot as plt

####Helper Functions####
def mean_calculator(MEAS: pd.DataFrame, lenses_per_nest: int=None) -> pd.DataFrame:
    """Calculate the desired means.
    Parameters:
    - MEAS (pd.DataFrame): Input DataFrame containing fiber measurements.
    - lenses_per_nest (int, optional): Number of lenses per nest for specific means calculation.
    If None, global means are calculated.
    Returns:
    pd.DataFrame: DataFrame containing mean values for fbx and fby.
    If lenses_per_nest is specified, it returns specific means for each position.
    Notes:
    If lenses_per_nest is None:
    - Calculates a global mean for fbx and fby.
    - Returns the mean values for both fbx and fby in a DataFrame.
    - Displays the mean values for fbx and fby.
    If lenses_per_nest is specified:
    - Calculates specific means for each position for fbx and fby based on the number of lenses per nest.
    - Returns a DataFrame containing specific mean values for fbx and fby for each position.
    - Displays the specific mean values for fbx and fby per position."""
    resume = MEAS.transpose().describe() #Transpose the df first due to describe() working in columns.
    rough_means = list(resume.iloc[1, :].values)
    means = []; means_fbx = []; means_fby = [] #Preallocation
    if lenses_per_nest == None: #Calculates a global mean for fbx and for fby
        for i, mean in enumerate(rough_means): #Iterates and rounds every mean value
            means_fbx.append(mean) if i % 2 == 0 else means_fby.append(mean)
            means.append(mean)
        abs_mean_fbx = sum(means_fbx) / len(means_fbx)
        abs_mean_fby = sum(means_fby) / len(means_fby)
        means = [abs_mean_fbx, abs_mean_fby]
        means_df = pd.DataFrame()
        df_list = []
        for _ in range(int(MEAS.shape[0])):  #Iterates over the whole measurements data
            nest_data = []
            for j in range(len(ordered_means)):
                value = float(ordered_means[j])
                nest_data.append(value)
            nest_df = pd.DataFrame({"mean": nest_data})
            df_list.append(nest_df)
        means_df = pd.concat(df_list, axis=0, ignore_index=True)
    else: #Calculates specific means for each position for fbx and fby
        mean_fbx = rough_means[0::2] #Gets fbx values
        mean_fby = rough_means[1::2] #Gets fby values
        for index in range(lenses_per_nest):
            specific_means = mean_fbx[index::lenses_per_nest] #Gets the values of the specific lens for fbx
            abs_mean_fbx = sum(specific_means) / len(specific_means)
            means_fbx.append(abs_mean_fbx)
            specific_means = mean_fby[index::lenses_per_nest] #Gets the values of the specific lens for fby
            abs_mean_fby = sum(specific_means) / len(specific_means)
            means_fby.append(abs_mean_fby)
        means = means_fbx + means_fby
        new_order = [0, 3, 1, 4, 2, 5]
        ordered_means = [means[i] for i in new_order] #Reorder of the means for implementation
        means_df = pd.DataFrame()
        df_list = []
        for _ in range(int(MEAS.shape[0] / (glob.lenses_per_nest * 2))):  #Iterates over every nest (e.g. 24/6=4 nests)
            nest_data = []
            for j in range(len(ordered_means)):
                value = float(ordered_means[j])
                nest_data.append(value)
            nest_df = pd.DataFrame({"mean": nest_data})
            df_list.append(nest_df)
        means_df = pd.concat(df_list, axis=0, ignore_index=True)
    return means_df

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

def plot_capability(measurements, analysis_table, label, sigma):
    ''''Plot a histogram with the values of a single fiber'''
    row = measurements.loc[label]
    mean = analysis_table.loc[label]["mean"]
    plt.hist(row.values, bins=30, edgecolor='black', alpha=0.7)
    try:
        low_limit = analysis_table.loc[label]['LO_LIMIT']
        high_limit = analysis_table.loc[label]['HI_LIMIT']
    except:
        low_limit = analysis_table.loc[label]['LSL']
        high_limit = analysis_table.loc[label]['USL']
    limits = [low_limit, high_limit]  # Replace with the positions where you want to draw lines
    for index, limit in enumerate(limits):
        legend_label = "Low Specification Level: " if index==0 else "High Specification Level: "
        plt.axvline(limit, color='red', linestyle='dashed', linewidth=2, label=f"{legend_label}{round(limit, 4)}")
    plt.axvline(mean, color='black', linestyle='dashed', linewidth=2, label=f"Average: {round(mean, 4)}")
    cal_low_limit = analysis_table.loc[label]['CAL_LO_LIMIT']
    cal_high_limit = analysis_table.loc[label]['CAL_HI_LIMIT']
    cal_limits = [cal_low_limit, cal_high_limit]  # Replace with the positions where you want to draw lines
    for index, cal_limit in enumerate(cal_limits):
        legend_label = "Minimun admisible value: " if index==0 else "Maximun admisible value: "
        plt.axvline(cal_limit, color='blue', linestyle='dashed', linewidth=2, label=f"{legend_label}{cal_limit}")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xlabel('Values')
    plt.ylabel('Frequency')
    plt.title(f'Values for: {label} (Sigma: {sigma})')
    plt.show()

def reset_df(df: pd.DataFrame) -> pd.DataFrame:
    df_2 = df.reset_index(drop=True)
    df_2.columns = [str(i) for i in range(df_2.shape[1])]
    return df_2

#Test script
if __name__ == '__main__':
    import os
    data = pd.read_excel(os.path.join(os.path.abspath("../a1_input"), "TOP_PASSAT_B9_2023y-11m-14d_17h-21m-03s.xlsx")) #Import the RyR generator output
    df = data.iloc[2:, 1:].reset_index(drop=True) #Slices measures and limits
    MEAS = reset_df(df.iloc[:, :-2])