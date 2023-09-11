import pandas as pd

s1 = pd.Series(['a', 'b'])
s2 = pd.Series(['c', 'd'])
data = pd.concat([s1, s2])
data = pd.concat([s1, s2], ignore_index=True)
print(data)