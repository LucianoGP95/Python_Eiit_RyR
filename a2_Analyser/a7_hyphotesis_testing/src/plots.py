import numpy as np
import matplotlib.pyplot as plt

def gaussian(mean: float, std_dev: float, test_sample: float=None, p_val: list=None):
    """
    Calculate the Gaussian probability density function.
    Parameters:
    mean (float): Mean of the Gaussian distribution.
    std_dev (float): Standard deviation of the Gaussian distribution.
    Returns:
    float or numpy.ndarray: Probability density value(s) of the Gaussian distribution.
    """
    x = np.linspace(mean-8*std_dev, mean+8*std_dev, 1000)  # Define the range of x values
    y = 1 / (std_dev * np.sqrt(2 * np.pi)) * np.exp(-((x - mean) ** 2) / (2 * std_dev ** 2))
    fig, ax = plt.subplots(figsize=(16,9))
    ax.plot(x, y, label='Gaussian Distribution')
    ax.set_xlabel('continuous Variable')
    ax.set_ylabel('Probability Density')
    ax.set_title('Parametrized Gaussian Distribution')
    ax.axhline(y=0, color="black", linestyle="-")
    ax.axvline(x=mean, color="gray", linestyle="--")
    ax.scatter(x=test_sample, y=1 / (std_dev * np.sqrt(2 * np.pi)) * np.exp(-((test_sample - mean) ** 2) / (2 * std_dev ** 2)), color="red") if test_sample is not None else None
    ax.legend()
    return fig

#Test script
if __name__ == "main":
    fig = gaussian(0, 1, 0.5)
    plt.show()
