# V2.0 
# 09/01/2025
# Added error handling to interface with teststand error handling

import os
import configparser

class MyConfigParser(configparser.ConfigParser):
    '''Custom class to stop the parser from converting upper cases to lower cases'''
    def optionxform(self, optionstr):
        return optionstr # do not change the case

def load_keys(filepath: str, section: str) -> list:
    try:
        config = MyConfigParser()
        config.read(filepath)
        keys_list = []
        section_data = config[section] 
        keys_list.extend([key.strip('"') for key in section_data.keys()])
        print("Section: \n" + section)
        print("Keys: ")
        print(keys_list)
        return keys_list
    except FileNotFoundError:
        print(f"Error: The file '{filepath}' was not found.")
    except Exception:
        print(f"An unexpected error occurred")
    return []

def load_values(filepath: str, section: str) -> list:
    try:
        config = MyConfigParser()
        config.read(filepath)
        values_list = []
        section_data = config[section] 
        values_list.extend([value.strip('"') for value in section_data.values()])
        print("Section: \n" + section)
        print("Values: ")
        print(values_list)
        return values_list
    except FileNotFoundError:
        print(f"Error: The file '{filepath}' was not found.")
    except Exception:
        print(f"An unexpected error occurred")
    return []

###Test Script
if __name__ == '__main__':
    filepath = "C:\CONTROLAR\RefCodes\Refcodes.ini"
    field = "RENAME"
    keys = load_keys(filepath, field)
    values = load_values(filepath, field)
