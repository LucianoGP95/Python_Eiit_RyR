import numpy as np

point = [0, 3.5]
limit_bars = ([0, 1], [0, 1, 2, 3, 4, 5])

def test(point, limit_bars):
    xx = [1, 2, 4]
    index = min(range(len(xx)), key=lambda i: abs(xx[i] - point[1]))
    position = xx[index]
    if point[1] > limit_bars[1][0]:
        print(limit_bars[1][position])
        print("True")

test(point, limit_bars)