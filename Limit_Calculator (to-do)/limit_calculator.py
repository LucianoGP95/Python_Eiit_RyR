import numpy as np
import matplotlib.pyplot as plt
import configparser

limits_path = './Limits/AUDI_Q2_PA.ini'
slope = 2

def limit_import(target_limit, limits_path):
    config = configparser.ConfigParser()
    config.read(limits_path)
    LIMIT = config['LIMITS_GENERIC'][target_limit]
    LIMIT = float(LIMIT[1:-1])
    return LIMIT

def line_plot(test_limit, string, plot_limits):
    '''Draws the simple, square aproximation, given the limit points.'''
    if "Y" in string:
        xx = np.linspace(plot_limits[0], plot_limits[1], 100)
        y = test_limit * np.ones(len(xx))
        plt.plot(xx, y, color='blue')
    elif "X" in string:
        plt.axvline(test_limit, color='red')

def rotated_plot(test_point, plot_limits, slope):
    xx = np.linspace(plot_limits[0], plot_limits[1], 100)
    y = slope * (xx - test_point[0]) + test_point[1]
    plt.plot(xx, y, color='blue')
    return y

LO_LIMIT_X = limit_import('Guia_Luz_Blanco_FB1_X_MIN', limits_path)
HI_LIMIT_X = limit_import('Guia_Luz_Blanco_FB1_X_MAX', limits_path)
LO_LIMIT_Y = limit_import('Guia_Luz_Blanco_FB1_Y_MIN', limits_path)
HI_LIMIT_Y = limit_import('Guia_Luz_Blanco_FB1_Y_MAX', limits_path)

print("Low limit x:", LO_LIMIT_X)
print("High limit x:", HI_LIMIT_X)
print("Low limit y:", LO_LIMIT_Y)
print("High limit y:", HI_LIMIT_Y)

xmin = LO_LIMIT_X - 0.05; xmax = HI_LIMIT_X + 0.05; ymin = LO_LIMIT_Y - 0.05; ymax = HI_LIMIT_Y + 0.05
plot_limits = (xmin, xmax, ymin, ymax)
#Simple plot
plt.xlim(xmin, xmax); plt.ylim(ymin, ymax)
line_plot(LO_LIMIT_X, "LO_LIMIT_X", plot_limits)
line_plot(HI_LIMIT_X, "HI_LIMIT_X", plot_limits)
line_plot(LO_LIMIT_Y, "LO_LIMIT_Y", plot_limits)
line_plot(HI_LIMIT_Y, "HI_LIMIT_Y", plot_limits)
plt.xlabel('fbx')
plt.ylabel('fby')
plt.title('Simple limits')
plt.show()
#Accurate plot
plt.xlim(xmin, xmax); plt.ylim(ymin, ymax)
line_plot(LO_LIMIT_X, "LO_LIMIT_X", plot_limits)
line_plot(HI_LIMIT_X, "HI_LIMIT_X", plot_limits)
y1 = rotated_plot(((LO_LIMIT_X + HI_LIMIT_X)/2, LO_LIMIT_Y), plot_limits, slope)
y2 = rotated_plot(((LO_LIMIT_X + HI_LIMIT_X)/2, HI_LIMIT_Y), plot_limits, slope)
plt.xlabel('fbx')
plt.ylabel('fby')
plt.title('Accurate limits')
point = [0.33, 0.35]
limit_bars = (y1, y2)
plt.scatter(point[0], point[1])
plt.show()

print(type(limit_bars))

def test(point, limit_bars): ######Finish
    '''Tests a single point, given limit bars'''
    xx = np.linspace(plot_limits[0], plot_limits[1], 100)
    index = min(range(len(xx)), key=lambda i: abs(xx[i] - point[1]))
    print(index)
    position = xx[index]
    print(limit_bars[0][index])
    if point[0] > limit_bars[0][index]:
        print("OK")
    else:
        print("NOK")

test(point, limit_bars)