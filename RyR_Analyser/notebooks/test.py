import matplotlib.pyplot as plt
import numpy as np
import sys
sys.path.append("../tools/")
import _db_tools as db

dbh = db.SQLite_Data_Extractor("database.db")
df = dbh.retrieve("measures")

# Assuming you have defined fibers, df, and legend_label earlier in your code

# Define a list of colormaps (one for each scatter plot)
colormaps = ['viridis', 'coolwarm', 'plasma', 'inferno']  # You can choose your colormaps

fibers = [1, 2, 3, 4]

# Loop through the fibers and create scatter plots with different colormaps
for i, fiber in enumerate(fibers):
    x_values = list(element + 1 for element in range(df.shape[1]))
    y_values = df.iloc[fiber - 1]
    
    # Use a different colormap for each scatter plot
    plt.scatter(
        x_values,
        y_values,
        cmap=colormaps[i % len(colormaps)]  # Cycle through the list of colormaps
    )

# Add a colorbar to the plot (optional)
plt.colorbar(label='Colorbar Label')

# Add labels, legends, and other plot decorations as needed
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.legend()

# Show the plot
plt.show()