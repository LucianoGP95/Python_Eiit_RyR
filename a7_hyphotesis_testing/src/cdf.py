import math

# Calculate the t-statistic
def norm_cdf(x, mu=0, sigma=1):
    """
    Compute the cumulative distribution function (CDF) of a normal distribution.
    
    Parameters:
    x (float): The value at which to evaluate the CDF.
    mu (float): The mean of the normal distribution (default is 0).
    sigma (float): The standard deviation of the normal distribution (default is 1).
    
    Returns:
    float: The CDF value at x.
    """
    return 0.5 + 0.5 * math.erf((x - mu) / (sigma * math.sqrt(2)))