import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 
        'purple', 'orange', 'brown', 'pink', 'gray', 'olive', 'cyan', 'darkred',
        'lightblue', 'lime', 'gold', 'indigo', 'seagreen', 'tomato', 'sienna', 'thistle']

###Main Functions
def plot_scatter(MEAS: pd.DataFrame, title=None, xlabel=None, ylabel=None, filter=None, limits: pd.DataFrame=None, yrange=None, add_tendency=False):
    """Plots a DataFrame as a scatter plot with optional filtering and customization.
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
        None"""
    fig, ax = plt.subplots(figsize=(12, 6))
    if filter is not None:
        filter = filter.upper() if isinstance(filter, str) else filter #Handles lower cases
    if filter == 'X':
        fibers = filter
        rows_to_plot = MEAS.iloc[0::2]  #Rows with odd indices
    elif filter == 'Y':
        fibers = filter
        rows_to_plot = MEAS.iloc[1::2]  #Rows with even indices
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
    slopes = []
    for index, row in rows_to_plot.iterrows():  #Plot the selected rows
        j += 1 if index % 2 == 0 else 0  #Increment j only on odd iterations (1, 1, 2, 2, ...)
        k += 1
        color = colors[index] if index < len(colors) else "blue"
        test = range(1, MEAS.shape[1] + 1)
        ax.scatter(test, row, color=color, label=_labeler(index, j, k, fibers=fibers))
        m = _add_tendency(ax, test, row, color) if add_tendency is True else None #Adds tendency lines for each row
        slopes.append(m)
    _format_plot(ax, title=title, xlabel=xlabel, ylabel=ylabel)
    _add_range(yrange=yrange) #Sets a unified range for the y plot axis
    if add_tendency == False:
        return fig
    else:
        return fig, slopes

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

def _draw_limits(fibers, LIMITS: pd.DataFrame, fixed_color: str=None):
    '''Small function to draw limits'''
    if LIMITS is not None and isinstance(LIMITS, pd.DataFrame):
        try:
            for i, fiber in enumerate(fibers):
                color1 = colors[i * 2 % len(colors)] if i < len(colors) else "orange"
                color2 = colors[(i * 2 + 1) % len(colors)] if i < len(colors) else "purple"
                label_low = f'Low limit: {fiber+1}'; label_high = f'High limit: {fiber+1}'
                if fixed_color is not None and isinstance(fixed_color, str):
                    color1 = fixed_color; color2 = fixed_color
                    label_low = "Specification limits"; label_high = None
                lo_limit = LIMITS.iloc[fiber, 0]
                hi_limit = LIMITS.iloc[fiber, 1]
                plt.axhline(y=lo_limit, color=color1, linestyle='--', label=label_low)
                plt.axhline(y=hi_limit, color=color2, linestyle='--', label=label_high)
        except Exception as e:
            print(f"Error adding limits: {e}")

def _add_tendency(ax, test, row, color):
    m, b = np.polyfit(test, row, 1)
    y = [m*x + b for x in test]
    ax.plot(test, y, linewidth=2, color=color)
    return m

def _format_plot(ax, title=None, xlabel=None, ylabel=None, set_legend=False):
    """Small function to give format to the plot."""
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if set_legend:
        ax.legend(loc='upper right', bbox_to_anchor=(1, 1))

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
