import pandas as pd
import numpy as np

# Sample DataFrame
data = {
    'A': [1, 2, 3, 4],
    'B': [10, 20, 30, 40],
    'C': [100, 200, 300, 400]
}

df = pd.DataFrame(data)

# Define a function to color cells
def color_cells(val):
    color = 'red' if val > 20 else 'green'
    return f'background-color: {color}'

# Apply the style
styled_df = df.style.applymap(color_cells)

# Display the styled DataFrame
styled_df
