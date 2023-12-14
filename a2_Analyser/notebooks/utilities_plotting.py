import pandas as pd
from globals import glob
import matplotlib.pyplot as plt

###Main Functions
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
        _draw_limits(fibers, limits)
    elif isinstance(filter, (list, tuple)):  #Fiber specified by sequence of integers
        fibers = [x - 1 for x in filter] #Get the correct index
        rows_to_plot = df.iloc[fibers]
        _draw_limits(fibers, limits)
    j = 0
    k = 0
    for index, row in rows_to_plot.iterrows():  #Plot the selected rows
        j += 1 if index % 2 == 0 else 0  #Increment j only on odd iterations (1, 1, 2, 2, ...)
        k += 1
        plt.scatter(
            list(range(1, df.shape[1] + 1)),
            row,
            label=_labeler(index, j, k, fibers=fibers)
        )
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.show()

def plot_capability(measurements, analysis_table, label, sigma):
    """Plot a histogram with specified limits and averages for a single fiber.
        Parameters:
        - measurements (pandas.DataFrame): DataFrame containing measurements for multiple fibers.
        - analysis_table (pandas.DataFrame): DataFrame containing analysis information for the specified fiber.
        - label (str): The label of the fiber for which the plot is generated.
        - sigma (float): The sigma value associated with the measurements.
        Returns:
        None
        This function generates a histogram for the specified fiber, overlaying it with vertical lines
        representing various limits and averages. The plot includes specification limits, calibration limits,
        the specified average, and the average of the fiber's measurements."""
    row = measurements.loc[label]
    mean = analysis_table.loc[label]["mean"] #Gets the specification means
    plt.hist(row.values, bins=30, edgecolor='black', alpha=0.7)
    try:
        low_limit = analysis_table.loc[label]['LO_LIMIT']
        high_limit = analysis_table.loc[label]['HI_LIMIT']
    except:
        low_limit = analysis_table.loc[label]['LSL']
        high_limit = analysis_table.loc[label]['USL']
    limits = [low_limit, high_limit]  #Replace with the positions where you want to draw lines
    for index, limit in enumerate(limits):
        legend_label = "Low Specification Level: " if index==0 else "High Specification Level: "
        plt.axvline(limit, color='red', linestyle='dashed', linewidth=2, label=f"{legend_label}{round(limit, 4)}")
    plt.axvline(mean, color='black', linestyle='dashed', linewidth=2, label=f"Specified average: {round(mean, 4)}") #Specification mean plotting
    cal_low_limit = analysis_table.loc[label]['CAL_LO_LIMIT']
    cal_high_limit = analysis_table.loc[label]['CAL_HI_LIMIT']
    cal_limits = [cal_low_limit, cal_high_limit]  #Replace with the positions where you want to draw lines
    for index, cal_limit in enumerate(cal_limits):
        legend_label = "Minimun admisible value: " if index==0 else "Maximun admisible value: "
        plt.axvline(cal_limit, color='blue', linestyle=':', linewidth=2, label=f"{legend_label}{cal_limit}")
    plt.axvline(row.mean(), color='green', linestyle=':', linewidth=2, label=f"Fiber average: {round(row.mean(), 4)}") #Fiber mean plotting
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xlabel('Values')
    plt.ylabel('Frequency')
    plt.title(f'Values for: {label} (Sigma: {sigma})')
    plt.show()

###Helper Functions
def _labeler(index, j, k, fibers=None):
    '''Small function to correctly label legends'''
    if fibers in ["X", "Y"]:
        axis = fibers
        label = f"Guia_Luz_Blanco_FB{k}_{axis}"
    elif isinstance(fibers, (list, tuple)):
        axis = "Y" if fibers[k-1] % 2 == 0 else "X"
        label = f"Fiber: {fibers[k-1]+1}"
    elif fibers == None:
        axis = "X" if index % 2 == 0 else "Y"
        label = f"Guia_Luz_Blanco_FB{j}_{axis}"
    return label

def _draw_limits(fibers, limits):
    '''Small function to draw limits'''
    if limits is not None and isinstance(limits, pd.DataFrame):
        colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
        try:
            for i, fiber in enumerate(fibers):
                color1 = colors[i * 2 % len(colors)] if i < len(colors) else "orange"
                color2 = colors[(i * 2 + 1) % len(colors)] if i < len(colors) else "purple"
                lo_limit = limits.iloc[fiber, 0]
                hi_limit = limits.iloc[fiber, 1]
                plt.axhline(y=lo_limit, color=color1, linestyle='--', label=f'Low limit: {fiber+1}')
                plt.axhline(y=hi_limit, color=color2, linestyle='--', label=f'High limit: {fiber+1}')
        except Exception as e:
            print(f"Error adding limits: {e}")

###Test Script
if __name__ == '__main__':
    import os, sys  ####Delete after debugging
    os.chdir(os.path.dirname(os.path.realpath(__file__)))  ####Delete after debugging
    import utilities_database as db
    measurements = db.retrieve_data("input.db", "TOP_PASSAT_B9_2023y_11m_14d_17h_21m_03s")
    limits = db.retrieve_data("input.db", "TOP_PASSAT_B9_limits_2023y_11m_14d_17h_21m_03s")
    plot_scatter(measurements, title='Scatter Plot, specific fiber(s)', xlabel='test', ylabel='MEAS', filter=[19, 20, 21], limits=limits)