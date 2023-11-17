import pandas as pd
from globals import glob
import matplotlib.pyplot as plt

####Helper Functions####
def plot_scatter(df, title=None, xlabel=None, ylabel=None, filter=None, limits=None):
    ''' Plots a DataFrame as a scatter plot with optional filtering and customization.
    Parameters:
        df (DataFrame): The input DataFrame containing the data.
        title (str, optional): The title of the plot.
        xlabel (str, optional): The label for the x-axis.
        ylabel (str, optional): The label for the y-axis.
        legend_label (str, optional): The label for the legend.
        filter (str, int, list, tuple, optional): Filter for selecting specific data points.
            - 'x' plots rows with odd indices.
            - 'y' plots rows with even indices.
            - None plots all rows.
            - int, list, or tuple selects specific row(s) based on the provided filter.
    Returns:
        None '''
    i = 0 #Preallocation
    if filter is not None:
        filter = filter.upper() if isinstance(filter, str) else filter #Handles lower cases
    if filter == 'X':
        fibers = filter
        rows_to_plot = df.iloc[1::2]  #Rows with odd indices
    elif filter == 'Y':
        fibers = filter
        rows_to_plot = df.iloc[::2]  #Rows with even indices
    elif filter is None:
        fibers = None
        rows_to_plot = df  #All rows
    elif isinstance(filter, int):  #Fiber specified by integer
        fibers = [x - 1 for x in [filter]]  #Get the correct index
        rows_to_plot = df.iloc[fibers]
        draw_limits(fibers, limits)
    elif isinstance(filter, (list, tuple)):  #Fiber specified by sequence of integers
        fibers = [x - 1 for x in filter] #Get the correct index
        rows_to_plot = df.iloc[fibers]
        draw_limits(fibers, limits)
    j = 0
    k = 0
    for index, row in rows_to_plot.iterrows():  #Plot the selected rows
        j += 1 if index % 2 == 0 else 0  #Increment j only on odd iterations (1, 1, 2, 2, ...)
        k += 1
        plt.scatter(
            list(range(1, df.shape[1] + 1)),
            row,
            label=labeler(index, j, k, fibers=fibers)
        )
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.show()

def labeler(index, j, k, fibers=None):
    '''Small function to correctly label legends'''
    if fibers in ["X", "Y"]:
        axis = fibers
        label = f"Guia_Luz_Blanco_FB{k}_{axis}"
    elif isinstance(fibers, (list, tuple)):
        axis = "Y" if fibers[k-1] % 2 == 0 else "X"
        #Calculate exact number of fiber in future
        label = f"Guia_Luz_Blanco_FB_{k}"
    elif fibers == None:
        axis = "X" if index % 2 == 0 else "Y"
        label = f"Guia_Luz_Blanco_FB{j}_{axis}"
    return label

def draw_limits(fibers, limits):
    '''Small function to draw limits'''
    if limits is not None and isinstance(limits, pd.DataFrame):
        try:
            for fiber in fibers:
                lo_limit = limits.iloc[fiber, 0]
                hi_limit = limits.iloc[fiber, 1]
            plt.axhline(y=lo_limit, color='r', linestyle='--', label='Low limit')
            plt.axhline(y=hi_limit, color='b', linestyle='--', label='High limit')
        except Exception as e:
            print(f"Error adding limits: {e}")