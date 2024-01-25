import os
from statistics import mean, stdev
import pandas as pd
import numpy as np
from globals import glob
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns
import pdfkit

colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 
        'purple', 'orange', 'brown', 'pink', 'gray', 'olive', 'cyan', 'darkred',
        'lightblue', 'lime', 'gold', 'indigo', 'seagreen', 'tomato', 'sienna', 'thistle']

###Main Functions
def plot_scatter(MEAS: pd.DataFrame, title=None, xlabel=None, ylabel=None, filter=None, limits: pd.DataFrame=None, yrange=None):
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
        ax.scatter(
            list(range(1, MEAS.shape[1] + 1)), row, color=color, label=_labeler(index, j, k, fibers=fibers))
    _format_plot(ax, title=title, xlabel=xlabel, ylabel=ylabel)
    _add_range(yrange=yrange) #Sets a unified range for the y plot axis
    return fig

def plot_control_chart(MEAS_format: pd.DataFrame, LIMITS: pd.DataFrame=None, title=None, xlabel=None, ylabel=None, fiber=None, yrange=None):
    try:
        row = MEAS_format.loc[fiber]
        fiber = [MEAS_format.index.get_loc(fiber)]
    except Exception:
        print("Error in the input label. Check the fiber written exists for the tooling.")
    sigma_low = mean(row) + 6*stdev(row)
    sigma_high = mean(row) - 6*stdev(row)
    _, ax = plt.subplots(figsize=(12, 6))
    ax.scatter(list(range(1, MEAS_format.shape[1] + 1)), row, label=fiber)
    ax.plot(list(range(1, MEAS_format.shape[1] + 1)), row, linestyle="-", color="red")
    _draw_limits(fiber, LIMITS, fixed_color="red")
    ax.axhline(y=sigma_low, color="blue", linestyle="--", label=f"Sigma limits")
    ax.axhline(y=sigma_high, color="blue", linestyle="--")
    _format_plot(ax, title=title, xlabel=xlabel, ylabel=ylabel, set_legend=True)
    _add_range(yrange=yrange) #Sets a unified range for the y plot axis
    plt.show()

def plot_boxplot(MEAS_format: pd.DataFrame, title: str="Fibers comparison", xlabel: str="Fiber",
                ylabel: str="Value", filter: str=None, lenses_per_nest: int=None):
    fig, ax = plt.subplots(figsize=(12, 6))
    if filter is not None:  #String filter
        filter = filter.upper() if isinstance(filter, str) else filter  #Handles lower cases
        xlabel += filter
        try:
            rows_to_plot = MEAS_format.loc[MEAS_format.index.str.contains(filter)]
        except AttributeError:
            rows_to_plot = MEAS_format.loc[:, MEAS_format.columns.str.contains(filter)]
    else:  #No filter
        rows_to_plot = MEAS_format
    if isinstance(filter, (int, list, tuple)):  #Fiber specified by numeric value
        rows_to_plot = MEAS_format.iloc[filter]
    if lenses_per_nest is not None and filter is not None:  #Renames columns for clarity when subgoruping lenses
        rows_to_plot.columns = [f"{i // lenses_per_nest + 1}-{(i % lenses_per_nest) + 1}" for i in range(rows_to_plot.shape[1])]
    else:
        rows_to_plot.columns = [i for i in range(1, rows_to_plot.shape[1] + 1)]
    sns.boxplot(data=rows_to_plot, orient='v', palette='Set3')
    _format_plot(ax, title=title, xlabel=xlabel, ylabel=ylabel, set_legend=False)
    return fig

def plot_capability(MEAS_format: pd.DataFrame, analysis_table: pd.DataFrame, 
                    label: str, sigma: int, xrange: list=None, figsize: tuple=(12, 6)):
    """Plot a histogram with specified limits and averages for a single fiber.
        Parameters:
        - measurements (pandas.DataFrame): DataFrame containing measurements for multiple fibers.
        - analysis_table (pandas.DataFrame): DataFrame containing analysis information for the specified fiber.
        - label (str): The label of the fiber for which the plot is generated.
        - sigma (int): The sigma value associated with the measurements.
        - xrange (list): Range for the x-axis.
        - figsize (tuple): Figure size in inches.
        Returns:
        Matplotlib Figure
        This function generates a histogram for the specified fiber, overlaying it with vertical lines
        representing various limits and averages. The plot includes specification limits, calibration limits,
        the specified average, and the average of the fiber's measurements."""
    try:
        row = MEAS_format.loc[label]
    except Exception:
        print("Error in the input label. Check the fiber written exists for the tooling.")
        return None
    fig, ax = plt.subplots(figsize=figsize)
    mean = analysis_table.loc[label]["mean"]  # Gets the specification means
    bins = 30
    ax.hist(np.round(row.values, 4), bins=bins, edgecolor='black', alpha=0.7)
    try:
        low_limit = analysis_table.loc[label]['LO_LIMIT']
        high_limit = analysis_table.loc[label]['HI_LIMIT']
    except:
        low_limit = analysis_table.loc[label]['LSL']
        high_limit = analysis_table.loc[label]['USL']
    limits = [low_limit, high_limit]  # Replace with the positions where you want to draw lines
    for index, limit in enumerate(limits):
        legend_label = "Low Specification Level: " if index == 0 else "High Specification Level: "
        ax.axvline(limit, color='red', linestyle='dashed', linewidth=2, label=f"{legend_label}{round(limit, 4)}")
    ax.axvline(mean, color='black', linestyle='dashed', linewidth=2, label=f"Specified average: {round(mean, 4)}")  # Specification mean plotting
    cal_low_limit = analysis_table.loc[label]['CAL_LO_LIMIT']
    cal_high_limit = analysis_table.loc[label]['CAL_HI_LIMIT']
    cal_limits = [cal_low_limit, cal_high_limit]  # Replace with the positions where you want to draw lines
    for index, cal_limit in enumerate(cal_limits):
        legend_label = "Minimum admissible value: " if index == 0 else "Maximum admissible value: "
        ax.axvline(cal_limit, color='blue', linestyle=':', linewidth=2, label=f"{legend_label}{cal_limit}")
    ax.axvline(row.mean(), color='green', linestyle=':', linewidth=2, label=f"Fiber average: {round(row.mean(), 4)}")  # Fiber mean plotting
    _format_plot(ax, title=f"Values for: {label} (Sigma: {sigma})", xlabel="Values", ylabel="Frequency")
    _add_range(ax, xrange=xrange)
    return fig

def plot_simple_limits(DATA_format: pd.DataFrame, nests_number: int, xrange: list=None,
                    yrange: list=None, limit_filter: [str, int]=None, fiber_filter=None, figsize: tuple=(12, 6)):
    """Draws a plot with simple, square approximations based on limit points and measurements.
    Parameters:
    - DATA_format (pd.DataFrame): The DataFrame containing measurement and limit data.
    - nests_number (int): The number of nests used for positioning limit points.
    - xrange (list, optional): The x-axis range for the plot. Default is None.
    - yrange (list, optional): The y-axis range for the plot. Default is None.
    - limit_filter (str or int, optional): Filter for specific limits based on position or index. Default is None.
    - fiber_filter (None or str): Filter for specific fiber measurements (None, 'X', or 'Y'). Default is None.
    Returns:
    - matplotlib.figure.Figure: The Figure object representing the generated plot.
    Note:
    - If 'limit_filter' is an integer, it selects a specific set of limits based on the position.
    - 'fiber_filter' can be used to filter measurements based on the fiber type ('X', 'Y').
    - If both 'xrange' and 'yrange' are provided, they set the plot limits accordingly.
    Example:
    fig = plot_simple_limits(DATA, nests_number=2, xrange=[0, 10], yrange=[-5, 5], limit_filter=1, fiber_filter='X')
    plt.show()"""
    positions = DATA_format.shape[0] // (nests_number * 2)
    MEAS = DATA_format.iloc[:, :-2]
    LIMITS = DATA_format.iloc[:, -2:]
    fig, ax = plt.subplots(figsize=figsize)
    if limit_filter is None:
        for index in range(positions * 2):
            if index % 2 == 0:
                x_limits = LIMITS.iloc[index]
                y_limits = LIMITS.iloc[index + 1]
                ax.hlines(y_limits.at["LO_LIMIT"], xmin=x_limits.at["LO_LIMIT"], xmax=x_limits.at["HI_LIMIT"],color=colors[index], linestyle='-')
                ax.hlines(y_limits.at["HI_LIMIT"], xmin=x_limits.at["LO_LIMIT"], xmax=x_limits.at["HI_LIMIT"],color=colors[index], linestyle='-')
                ax.vlines(x_limits.at["LO_LIMIT"], ymin=y_limits.at["LO_LIMIT"], ymax=y_limits.at["HI_LIMIT"],color=colors[index], linestyle='-')
                ax.vlines(x_limits.at["HI_LIMIT"], ymin=y_limits.at["LO_LIMIT"], ymax=y_limits.at["HI_LIMIT"],color=colors[index], linestyle='-')
    elif isinstance(limit_filter, int):
        mapping = {i: 2 * (i - 1) for i in range(1, positions + 1)}  # Maps input values to the LIMITS indexers
        limit_position = mapping.get(limit_filter, None)
        x_limits = LIMITS.iloc[limit_position]
        y_limits = LIMITS.iloc[limit_position + 1]
        ax.hlines(y_limits.at["LO_LIMIT"], xmin=x_limits.at["LO_LIMIT"], xmax=x_limits.at["HI_LIMIT"], color="r",linestyle='-')
        ax.hlines(y_limits.at["HI_LIMIT"], xmin=x_limits.at["LO_LIMIT"], xmax=x_limits.at["HI_LIMIT"], color="r",linestyle='-')
        ax.vlines(x_limits.at["LO_LIMIT"], ymin=y_limits.at["LO_LIMIT"], ymax=y_limits.at["HI_LIMIT"], color="r",linestyle='-')
        ax.vlines(x_limits.at["HI_LIMIT"], ymin=y_limits.at["LO_LIMIT"], ymax=y_limits.at["HI_LIMIT"], color="r",linestyle='-')
    for index in range(MEAS.shape[0]):
        if fiber_filter is not None and "X" in fiber_filter:
            fiber_index = DATA_format.index.get_loc(fiber_filter)
            x_values = MEAS.iloc[fiber_index]
            y_values = MEAS.iloc[fiber_index + 1]
            ax.scatter(x_values, y_values)
        elif fiber_filter is not None and "Y" in fiber_filter:
            fiber_index = DATA_format.index.get_loc(fiber_filter)
            x_values = MEAS.iloc[fiber_index]
            y_values = MEAS.iloc[fiber_index - 1]
            ax.scatter(x_values, y_values)
        else:
            if index % 2 == 0:
                x_values = MEAS.iloc[index]
                y_values = MEAS.iloc[index + 1]
                ax.scatter(x_values, y_values)
    _format_plot(ax, title='Measurements versus limits', xlabel='X measurement', ylabel='Y measurement', set_legend=False)
    _add_range(ax, xrange=xrange, yrange=yrange)
    return fig

def plot_to_pdf(df: list[pd.DataFrame], name: str="Capability_report.pdf", plot: str=None):
    plot = plot.upper() if isinstance(plot, str) else None
    if plot == "SCATTER":
        new_index = 0
        with PdfPages(os.path.join("..\\a2_output\\reports", name)) as pdf:
            fig = plot_scatter(df, title='Scatter Plot, all fibers', xlabel='test', ylabel='MEAS') #Plot all guides
            pdf.savefig(fig)
            plt.close(fig)
            fig = plot_scatter(df, title='Scatter Plot, fiber X', xlabel='test', ylabel='MEAS', filter='x') #Plot x axis values
            pdf.savefig(fig)
            plt.close(fig)
            fig = plot_scatter(df, title='Scatter Plot, fiber Y', xlabel='test', ylabel='MEAS', filter='y') #Plot y axis values
            pdf.savefig(fig)
            plt.close(fig)
        return True
    if plot == "BOXPLOT":
        new_index = 0
        with PdfPages(os.path.join("..\\a2_output\\reports", name)) as pdf:
            fig = plot_boxplot(df[0], title="Fibers values versus test number", xlabel="Test number", ylabel="Value", filter=None)
            pdf.savefig(fig)
            plt.close(fig)
            fig = plot_boxplot(df[0], title="Fibers values versus test number, X-axis", xlabel="Test number: ", ylabel="Value", filter="X")
            pdf.savefig(fig)
            plt.close(fig)
            fig = plot_boxplot(df[0], title="Fibers values versus test number, Y-axis", xlabel="Test number: ", ylabel="Value", filter="Y")
            pdf.savefig(fig)
            plt.close(fig)
            fig = plot_boxplot(df[0].transpose(), title="Fibers values versus lens group, X-axis", xlabel="Lens groups: ", ylabel="Value", filter="X", lenses_per_nest=int(df[1].loc["Lenses per nest", "Tooling data"]))
            pdf.savefig(fig)
            plt.close(fig)
            fig = plot_boxplot(df[0].transpose(), title="Fibers values versus lens group, Y-axis", xlabel="Lens groups: ", ylabel="Value", filter="Y", lenses_per_nest=int(df[1].loc["Lenses per nest", "Tooling data"]))
            pdf.savefig(fig)
            plt.close(fig)
        return True
    if plot == "CAPABILITY":
        new_index = 0
        with PdfPages(os.path.join("..\\a2_output\\reports", name)) as pdf:
            for index in range(df[0].shape[0]):
                new_index += 1 if index % 2 == 0 else 0  #Increment new_index only on odd iterations
                axis = "X" if index % 2 == 0 else "Y"
                title = f"Guia_Luz_Blanco_FB{new_index}_{axis}"
                fig = plot_capability(df[0], df[1], title, 6, xrange=[0.3, 0.36], figsize=(12, 8))
                pdf.savefig(fig)
                plt.close(fig)
        return True
    if plot == "AXIS":
        new_index = 0
        with PdfPages(os.path.join("..\\a2_output\\reports", name)) as pdf:
            fig = plot_simple_limits(df, glob.nests_number, xrange=None, yrange=None,
                                    limit_filter=None, fiber_filter=None, figsize=(12, 8))
            pdf.savefig(fig)
            plt.close(fig)
        return True
    else:
        raise ValueError("Unsupported plot type. Try 'Capability'.")

def df_to_pdf(df, name_data):
    temp_name = glob.tooling + "_data_" + ".jpg"
    fig, ax = plt.subplots(figsize=(8, 4)) 
    ax.axis('tight')
    ax.axis('off')
    ax.table(cellText=df.values, colLabels=df.columns, cellLoc = 'center', loc='center')
    plt.savefig(os.path.abspath(os.path.join("..\\a2_output\\reports", temp_name)))
    pdfkit.from_file(os.path.abspath(os.path.join("..\\a2_output\\reports", temp_name)), name_data)
    os.remove(os.path.abspath(os.path.join("..\\a2_output\\reports", temp_name)))

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

###Test Script
if __name__ == '__main__':
    import os, sys  ####Delete after debugging
    os.chdir(os.path.dirname(os.path.realpath(__file__)))  ####Delete after debugging
    import utilities_database as db
    measurements = db.retrieve_data("input.db", "TOP_PASSAT_B9_2023y_11m_14d_17h_21m_03s")
    limits = db.retrieve_data("input.db", "TOP_PASSAT_B9_limits_2023y_11m_14d_17h_21m_03s")
    plot_scatter(measurements, title='Scatter Plot, specific fiber(s)', xlabel='test', ylabel='MEAS', filter=[19, 20, 21], limits=limits)