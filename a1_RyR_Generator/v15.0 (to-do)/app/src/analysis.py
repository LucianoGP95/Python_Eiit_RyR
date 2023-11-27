import os
import pandas as pd
import numpy as np

def generate_RyR(df):
    """
    Generate RyR data for the given dataframe
    """
    resume = df.transpose().describe().transpose() #Transpose the df first due to describe() working in columns.
    print(resume)