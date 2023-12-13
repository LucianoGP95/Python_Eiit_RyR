import pandas as pd
from utilities_plotting import plot_scatter

def import_file(filepath):
    df = pd.read_excel(filepath)
    return df

def plot(df, filter):
    try:
        int(filter)
    except Exception as e:
        print(f"Cannot convert filter: {e}")
    print(filter)
    plot_scatter(df, title=None, xlabel=None, ylabel=None, filter=filter, limits=None)