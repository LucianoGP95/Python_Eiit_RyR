import os
import pandas as pd
import numpy as np
from globals import glob
import configparser
import matplotlib.pyplot as plt

####Main Functions
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
        for i in range(int(MEAS.shape[0])):  #Iterates over the whole measurements data
            fiber_mean = means[0] if i % 2 == 0 else means[1]
            df_iteration = pd.DataFrame({'mean': [fiber_mean]})
            df_list.append(df_iteration)
        means_df = pd.concat(df_list, axis=0, ignore_index=False)
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
        means_df = pd.concat(df_list, axis=0, ignore_index=False)
    means_df.reset_index(drop=True, inplace=True)
    return means_df

def limits_generator(means_df: pd.DataFrame) -> pd.DataFrame:
    """Generate lower and upper tolerance limits based on the means provided in the DataFrame.
    Parameters:
    - means_df (pd.DataFrame): A DataFrame containing a column 'mean' with mean values for each row.
    Returns:
    - pd.DataFrame: A DataFrame with columns 'LO_LIMIT' and 'HI_LIMIT', representing the lower and upper
    tolerance limits calculated based on the mean values. The limits are adjusted depending on the row index:
    - If the index is even, the limits are calculated with x_tolerance.
    - If the index is odd, the limits are calculated with y_tolerance."""
    x_tolerance = glob.x_tolerance
    y_tolerance = glob.y_tolerance
    low_limits = []
    high_limits = []
    for index, row in means_df.iterrows():
        if index % 2 == 0:
            low_limit = row['mean'] - x_tolerance  # Adjusted calculation based on index parity
            high_limit = row['mean'] + x_tolerance
        else:
            low_limit = row['mean'] - y_tolerance
            high_limit = row['mean'] + y_tolerance
        low_limits.append(low_limit)
        high_limits.append(high_limit)
    limits_df = pd.DataFrame({"LO_LIMIT": low_limits, "HI_LIMIT": high_limits})
    return limits_df

def ini_generator(limits: pd.DataFrame, lenses_per_nest: int, nests_number: int) -> None:
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
    >>> ini_generator(limits_df, 3)'''
    class CaseSensitiveConfigParser(configparser.ConfigParser):
        '''A custom class to override optionxform and avoid uppercases being converted to lowercases.'''
        def optionxform(self, optionstr):
            return optionstr
    config = CaseSensitiveConfigParser()
    if lenses_per_nest == 3 and nests_number == 4: #Import a template based on the number of lenses per nest
        config.read('../data/template_12_fibers.ini')
    elif lenses_per_nest == 4 and nests_number == 4:
        config.read('../data/template_16_fibers.ini')
    elif lenses_per_nest == 3 and nests_number == 2:
        config.read('../data/template_6_fibers.ini')
    else:
        raise ValueError("lenses_per_nest should be 3 or 4.")
    keys_list = []
    for section_name in config.sections(): #Get a keys list with the correct uppercased keys
        section = config[section_name]
        keys_list.extend(section.keys())
    for section in config.sections(): #Iterate through the sections and options in the .ini file
        keys_list = list(config[section].keys())
        j = 0
        for i in range(0, len(keys_list), 2):
            key1 = keys_list[i]
            key2 = keys_list[i + 1]
            col1 = str(round(limits.iloc[j, 1], 4))
            col2 = str(round(limits.iloc[j, 0], 4))
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
    save_path = os.path.abspath(f'../a2_output/{glob.tooling}.ini')
    with open(save_path, 'w') as configfile:
        for section in config.sections():
            configfile.write(f"[{section}]\n")
            keys = keys_list  #Recover the original keys to write them in the .ini file
            for i, key in enumerate(keys):
                configfile.write(f"{key} = {config[section][key]}\n")
                if (i + 1) % 4 == 0 and i < len(keys) - 1:  #Insert a blank line every four keys
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
    measures = df.iloc[:, :-2]  
    limits = df.iloc[:, -2:]  
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

def capability_calculation(specifications: pd.DataFrame, sigma: int) -> pd.DataFrame:
    """
    Calculate process capability indices (Cp and Cpk) for fiber-related specifications.
    Parameters:
    - specifications (pd.DataFrame): DataFrame containing fiber-related specifications including columns:
        - "fiber mean": Mean of the fiber measurements.
        - "std": Standard deviation of the fiber measurements.
        - "LSL": Lower Specification Limit.
        - "USL": Upper Specification Limit.
    - sigma (int): Number of standard deviations used to determine the process capability.
    Returns:
    pd.DataFrame: DataFrame containing the original specifications along with additional columns:
    - "CAL_LO_LIMIT": Calculated lower limit based on the specified sigma.
    - "CAL_HI_LIMIT": Calculated upper limit based on the specified sigma.
    - "Cp": Process capability index.
    - "Cpk": Process capability index corrected for asymmetry.
    The Cp is calculated as (USL - LSL) / (sigma * std), where std is the standard deviation.
    The Cpk is the minimum of two indices, one for the lower specification limit and one for the upper specification limit.
    It is calculated as the minimum of (fiber mean - LSL) / ((sigma/2) * std) and (USL - fiber mean) / ((sigma/2) * std)."""
    capabilities = []; capabilities_corrected = []; low_limits = []; high_limits = []
    for _, row in specifications.iterrows():
        fiber_mean = row["fiber mean"]  
        std = row["std"]
        LSL = row["LSL"]
        USL = row["USL"]
        low_limit = fiber_mean - (1/2) * (sigma * std)
        high_limit = fiber_mean + (1/2) * (sigma * std)
        Cp = (USL - LSL) / (sigma * std)
        Cpl = (fiber_mean - LSL) / ((sigma/2 * std))
        Cph = (USL - fiber_mean) / ((sigma/2 * std))
        Cpk = min(Cpl, Cph)
        low_limits.append(round(low_limit, 4))
        high_limits.append(round(high_limit, 4))
        capabilities.append(Cp)
        capabilities_corrected.append(Cpk)
    capabilities = pd.DataFrame(capabilities, columns=["Cp"])
    capabilities_corrected = pd.DataFrame(capabilities_corrected, columns=["Cpk"])
    low_limits = pd.DataFrame(low_limits, columns=["CAL_LO_LIMIT"])
    high_limits = pd.DataFrame(high_limits, columns=["CAL_HI_LIMIT"])
    analysis = pd.concat([specifications, low_limits, high_limits, capabilities, capabilities_corrected], axis=1)
    return analysis

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