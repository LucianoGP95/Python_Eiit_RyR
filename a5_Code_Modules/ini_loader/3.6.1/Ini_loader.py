import os
import configparser

class MyConfigParser(configparser.ConfigParser):
    '''Custom class to stop the parser from converting upper cases to lower cases'''
    def optionxform(self, optionstr):
        return optionstr # do not change the case

def load_keys(filepath: str, section: str) -> list:
    config = MyConfigParser()
    config.read(filepath)
    keys_list = []
    section_data = config[section] 
    print(type(section_data))
    keys_list.extend([key.strip('"') for key in section_data.keys()])
    print("Section: \n" + section)
    print("Keys: ")
    print(keys_list)
    return keys_list

def load_values(filepath: str, section: str) -> list:
    config = MyConfigParser()
    config.read(filepath)
    values_list = []
    section_data = config[section] 
    values_list.extend([value.strip('"') for value in section_data.values()])
    print("Section: \n" + section)
    print("Values: ")
    print(values_list)
    return values_list

###Test
filepath = "C:\CONTROLAR\RefCodes\Refcodes.ini"
field = "VA-007"
keys = load_keys(filepath, field)
values = load_values(filepath, field)
