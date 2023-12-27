import pandas as pd
import numpy as np
from globals import glob
import matplotlib.pyplot as plt
import seaborn as sns

colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 
        'purple', 'orange', 'brown', 'pink', 'gray', 'olive', 'cyan', 'darkred',
        'lightblue', 'lime', 'gold', 'indigo', 'seagreen', 'tomato', 'sienna', 'thistle']

###Main Functions
def plot_scatter(MEAS: pd.DataFrame, title=None, xlabel=None, ylabel=None, filter=None, limits: pd.DataFrame=None, yrange=None):
    ''' Plots a DataFrame as a scatter plot with optional filtering and customization.
    Parameters:
        MEAS (DataFrame): The input DataFrame containing the data.
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
        rows_to_plot = MEAS.iloc[1::2]  #Rows with odd indices
    elif filter == 'Y':
        fibers = filter
        rows_to_plot = MEAS.iloc[::2]  #Rows with even indices
    elif filter is None:
        fibers = None
        rows_to_plot = MEAS  #All rows
    elif isinstance(filter, int):  #Fiber specified by integer
        fibers = [x - 1 for x in [filter]]  #Get the correct index
        rows_to_plot = MEAS.iloc[fibers]
        _draw_limits(fibers, limits)
    elif isinstance(filter, (list, tuple)):  #Fiber specified by sequence of integers
        fibers = [x - 1 for x in filter] #Get the correct index
        rows_to_plot = MEAS.iloc[fibers]
        _draw_limits(fibers, limits)
    j = 0
    k = 0
    for index, row in rows_to_plot.iterrows():  #Plot the selected rows
        j += 1 if index % 2 == 0 else 0  #Increment j only on odd iterations (1, 1, 2, 2, ...)
        k += 1
        color = colors[index] if index < len(colors) else "blue"
        plt.scatter(
            list(range(1, MEAS.shape[1] + 1)), row, color=color, label=_labeler(index, j, k, fibers=fibers))
    _format_plot(title=title, xlabel=xlabel, ylabel=ylabel)
    _add_range(yrange=yrange) #Sets a unified range for the y plot axis
    plt.show()

def plot_control_chart(MEAS_format: pd.DataFrame, LIMITS: pd.DataFrame=None, title=None, xlabel=None, ylabel=None, fiber=None, yrange=None):
    try:
        row = MEAS_format.loc[fiber]
    except Exception:
        print("Error in the input label. Check the fiber written exists for the tooling.")
    plt.scatter(list(range(1, MEAS_format.shape[1] + 1)), row, label=fiber)
    plt.plot(list(range(1, MEAS_format.shape[1] + 1)), row, linestyle='-', color='red')
    _format_plot(title=title, xlabel=xlabel, ylabel=ylabel, legend=False)
    _draw_limits([0], LIMITS)
    _add_range(yrange=yrange) #Sets a unified range for the y plot axis
    plt.show()

def deprecated_plot_boxplot(MEAS_format: pd.DataFrame, title="Fibers comparison", xlabel="Fiber", ylabel="Value", filter: str=None):
    if filter is not None:
        filter = filter.upper() if isinstance(filter, str) else filter #Handles lower cases
    if filter == 'X':
        rows_to_plot = MEAS_format.iloc[1::2]  #Rows with odd indices
        labels = rows_to_plot.index
    elif filter == 'Y':
        rows_to_plot = MEAS_format.iloc[::2]  #Rows with even indices
        labels = rows_to_plot.index
    elif filter is None:
        rows_to_plot = MEAS_format  #All rows
        labels = [item for item in rows_to_plot.index]
    elif isinstance(filter, (int, list, tuple)):  #Fiber specified by integer
        rows_to_plot = MEAS_format.iloc[filter]
        labels = [item for item in rows_to_plot.index]
    plt.boxplot(rows_to_plot.transpose(), labels=labels)
    _format_plot(title=title, xlabel=xlabel, ylabel=ylabel, legend=False)
    plt.show()

def plot_boxplot(MEAS_format: pd.DataFrame, title: str="Fibers comparison", xlabel: str="Fiber", ylabel: str="Value", filter: str=None):
    if filter is not None: #String filter
        filter = filter.upper() if isinstance(filter, str) else filter  #Handles lower cases
        xlabel = xlabel+filter
        try:
            array = MEAS_format.index.str.contains(filter)
        except:
            array = None
        if array is not None:  #Handles transposition in the MEAS df argument
            rows_to_plot = MEAS_format.loc[MEAS_format.index.str.contains(filter)]
        else:
            rows_to_plot = MEAS_format.loc[:, MEAS_format.columns.str.contains(filter)]
    elif filter is None: #No filter
        rows_to_plot = MEAS_format  
    elif isinstance(filter, (int, list, tuple)):  #Fiber specified by numeric value
        rows_to_plot = MEAS_format.iloc[filter]
    rows_to_plot.columns = [i for i in range(1, rows_to_plot.shape[1] + 1)] #Renames columns for clarity
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=rows_to_plot, orient='v', palette='Set3')
    _format_plot(title=title, xlabel=xlabel, ylabel=ylabel, legend=False)
    plt.show()

def plot_capability(MEAS_format: pd.DataFrame, analysis_table: pd.DataFrame, label: str, sigma: int, xrange=None):
    """Plot a histogram with specified limits and averages for a single fiber.
        Parameters:
        - measurements (pandas.DataFrame): DataFrame containing measurements for multiple fibers.
        - analysis_table (pandas.DataFrame): DataFrame containing analysis information for the specified fiber.
        - label (str): The label of the fiber for which the plot is generated.
        - sigma (int): The sigma value associated with the measurements.
        Returns:
        None
        This function generates a histogram for the specified fiber, overlaying it with vertical lines
        representing various limits and averages. The plot includes specification limits, calibration limits,
        the specified average, and the average of the fiber's measurements."""
    try:
        row = MEAS_format.loc[label]
    except Exception:
        print("Error in the input label. Check the fiber written exists for the tooling.")
    mean = analysis_table.loc[label]["mean"] #Gets the specification means
    bins = 30
    plt.hist(np.round(row.values, 4), bins=bins, edgecolor='black', alpha=0.7)
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
    _format_plot(title=f'Values for: {label} (Sigma: {sigma})', xlabel='Values', ylabel='Frequency')
    _add_range(xrange=xrange) #Sets a unified range for the x plot axis
    plt.show()

def plot_simple_limits(DATA_format: pd.DataFrame, nests_number: int, xrange: list=None, yrange: list=None, limit_filter: [str, int]=None):
    '''Draws the simple, square aproximation, given the limit points.'''
    positions = DATA_format.shape[0] // (nests_number * 2)
    MEAS = DATA_format.iloc[:, :-2]; LIMITS = DATA_format.iloc[:, -2:]
    if limit_filter is None:
        for index in range(positions*2):
            if index % 2 == 0:
                x_limits = LIMITS.iloc[index]
                y_limits = LIMITS.iloc[index + 1]
                plt.hlines(y_limits.at["LO_LIMIT"], xmin=x_limits.at["LO_LIMIT"], xmax=x_limits.at["HI_LIMIT"], color=colors[index], linestyle='-')
                plt.hlines(y_limits.at["HI_LIMIT"], xmin=x_limits.at["LO_LIMIT"], xmax=x_limits.at["HI_LIMIT"], color=colors[index], linestyle='-')
                plt.vlines(x_limits.at["LO_LIMIT"], ymin=y_limits.at["LO_LIMIT"], ymax=y_limits.at["HI_LIMIT"], color=colors[index], linestyle='-')
                plt.vlines(x_limits.at["HI_LIMIT"], ymin=y_limits.at["LO_LIMIT"], ymax=y_limits.at["HI_LIMIT"], color=colors[index], linestyle='-')
    elif isinstance(limit_filter, int):
        mapping = {i: 2 * (i - 1) for i in range(1, positions + 1)} #Maps input values to the LIMITS indexers
        limit_position = mapping.get(limit_filter, None)
        x_limits = LIMITS.iloc[limit_position]
        y_limits = LIMITS.iloc[limit_position + 1]
        plt.hlines(y_limits.at["LO_LIMIT"], xmin=x_limits.at["LO_LIMIT"], xmax=x_limits.at["HI_LIMIT"], color="r", linestyle='-')
        plt.hlines(y_limits.at["HI_LIMIT"], xmin=x_limits.at["LO_LIMIT"], xmax=x_limits.at["HI_LIMIT"], color="r", linestyle='-')
        plt.vlines(x_limits.at["LO_LIMIT"], ymin=y_limits.at["LO_LIMIT"], ymax=y_limits.at["HI_LIMIT"], color="r", linestyle='-')
        plt.vlines(x_limits.at["HI_LIMIT"], ymin=y_limits.at["LO_LIMIT"], ymax=y_limits.at["HI_LIMIT"], color="r", linestyle='-')
    for index in range(MEAS.shape[0]):
        if index % 2 == 0:
            x_values = MEAS.iloc[index]
            y_values = MEAS.iloc[index + 1]
            plt.scatter(x_values, y_values)
    _format_plot(title='Measurements versus limits', xlabel='X measurement', ylabel='Y measurement', legend=False)
    _add_range(xrange=xrange, yrange=yrange) #Sets a unified range for the x and y plot axis
    plt.show()

###Hidden Functions
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

def _draw_limits(fibers, LIMITS: pd.DataFrame):
    '''Small function to draw limits'''
    if LIMITS is not None and isinstance(LIMITS, pd.DataFrame):
        try:
            for i, fiber in enumerate(fibers):
                color1 = colors[i * 2 % len(colors)] if i < len(colors) else "orange"
                color2 = colors[(i * 2 + 1) % len(colors)] if i < len(colors) else "purple"
                lo_limit = LIMITS.iloc[fiber, 0]
                hi_limit = LIMITS.iloc[fiber, 1]
                plt.axhline(y=lo_limit, color=color1, linestyle='--', label=f'Low limit: {fiber+1}')
                plt.axhline(y=hi_limit, color=color2, linestyle='--', label=f'High limit: {fiber+1}')
        except Exception as e:
            print(f"Error adding limits: {e}")

def _format_plot(title=None, xlabel=None, ylabel=None, legend=True):
    '''Small function to give format to the plot'''
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left') if legend == True else None

def _add_range(xrange: list=None, yrange: list=None):
    '''Small function to set plot limits'''
    if yrange is None and xrange is not None:
        plt.xlim(xrange[0], xrange[1])
    elif xrange is None and yrange is not None:
        plt.ylim(yrange[0], yrange[1])
    elif xrange is not None and yrange is not None:
        plt.ylim(yrange[0], yrange[1])
        plt.xlim(xrange[0], xrange[1])
    else: 
        pass

###Test Script
if __name__ == '__main__':
    import os, sys  ####Delete after debugging
    os.chdir(os.path.dirname(os.path.realpath(__file__)))  ####Delete after debugging
    import utilities_database as db
    measurements = db.retrieve_data("input.db", "TOP_PASSAT_B9_2023y_11m_14d_17h_21m_03s")
    limits = db.retrieve_data("input.db", "TOP_PASSAT_B9_limits_2023y_11m_14d_17h_21m_03s")
    plot_scatter(measurements, title='Scatter Plot, specific fiber(s)', xlabel='test', ylabel='MEAS', filter=[19, 20, 21], limits=limits)