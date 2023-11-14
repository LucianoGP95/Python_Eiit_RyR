import pandas as pd
import numpy as np

def format_output(df: pd.DataFrame) -> pd.DataFrame:
    columns_number = df.shape[1]
    df.columns = range(columns_number)  #Resets columns
    new_column_names = { #Create a dictionary for renaming
        0: "Guía de luz", 
        columns_number - 2: "LO_LIMIT", 
        columns_number - 1: "HI_LIMIT"
    }
    df.rename(columns=new_column_names, inplace=True)
    df.reset_index() #Reset index
    return df