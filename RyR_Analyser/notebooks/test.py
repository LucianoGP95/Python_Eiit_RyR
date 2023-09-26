import configparser

class CaseSensitiveConfigParser(configparser.ConfigParser):
    def optionxform(self, optionstr):
        return optionstr
config = CaseSensitiveConfigParser()
config.read('../data/template.ini')
keys_list = []

# Iterate through sections and add keys to the list
for section_name in config.sections():
    section = config[section_name]
    keys_list.extend(section.keys())

# Now, keys_list contains all the keys from the INI file, preserving case
print(keys_list)
