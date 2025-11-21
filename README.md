# Pyramid Plot

A Python package for creating pyramid plots using Matplotlib.

## Installation

```bash
pip install pyramidplot
```

## Usage

### Using DataFrame

```python
import pandas as pd
import matplotlib.pyplot as plt
from pyramidplot import pyramidplot

# Sample data
levels = ["Producers", "Primary Consumers", "Secondary Consumers", "Tertiary Consumers"]
values = [800, 400, 200, 150]

data = pd.DataFrame({
    "Level": levels,
    "Value": values
})

# Create plot
fig, ax = plt.subplots(figsize=(8, 6))
pyramidplot(
    data, 
    var_levels="Level", 
    var_values="Value", 
    ax=ax, 
    show_trend=True, 
    edgecolor='none',
    label_color='black',
    trend_color='gray'
)

plt.show()
```
![Pyramid Plot Demo](https://github.com/bioinfoguru/pyramidplot/blob/main/demo_plot.png?raw=true)

### Using Lists

```python
import matplotlib.pyplot as plt
from pyramidplot import pyramidplot

levels = ["Producers", "Primary Consumers", "Secondary Consumers", "Tertiary Consumers"]
values = [800, 400, 200, 150]

fig, ax = plt.subplots(figsize=(8, 6))
pyramidplot(
    levels, 
    values, 
    ax=ax, 
    show_trend=True,
    edgecolor='none',
    label_color='black',
    trend_color='gray'
)
plt.show()
```

## Features

- **Custom Levels and Values**: Takes a DataFrame or two lists (levels, values).
- **Matplotlib Polygons**: Uses `Polygon` patches to draw the pyramid levels (trapezoids).
- **Colormap Support**: Allows specifying a colormap for level coloring.
- **Labels**: Options to label levels and values.
- **Label Color**: Option to specify label color or use the level color (default).
- **Trend Overlay**: Option to show arrows and percentage change between levels (centered with labels, smaller size, padded).
- **Trend Color**: Option to specify color for trend arrows and text (default 'gray').
- **Invert Trend**: Use `invert_trend=True` (boolean) to invert trend arrows (downwards) and percentage sign (positive for loss).
- **Edge Customization**: Option to customize or remove polygon edges using `edgecolor`.
