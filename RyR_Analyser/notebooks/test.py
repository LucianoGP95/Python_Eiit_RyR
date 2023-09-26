import configparser
import pandas as pd

limits = pd.DataFrame([[0.324, 0.3541, 0.333, 0.3572, 0.3452, 0.3707, 0.3247, 0.3519, 0.3322, 0.3586, 0.3365, 0.3656], [0.3248, 0.3538, 0.3302, 0.3588, 0.3435, 0.3688, 0.3324, 0.3593, 0.3385, 0.3623, 0.3512, 0.3728]]).transpose()
print(limits)

##Creation of the .ini
#Create a ConfigParser instance and read the .ini file
config = configparser.ConfigParser()
config.read('../data/template.ini')

#Iterate through the sections and options in the .ini file
HI_LIMIT = limits.iloc[:, 1]
LO_LIMIT = limits.iloc[:, 0]
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

#Loop through the sections and options in the .ini file and print them
for section in config.sections():
    print(f"[{section}]")
    for key, value in config.items(section):
        print(f"{key} = {value}")

#Save the modified data to a new .ini file
with open('../output/limits.ini', 'w') as configfile:
    config.write(configfile)