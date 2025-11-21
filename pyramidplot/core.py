import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, FancyArrowPatch
import numpy as np
import pandas as pd

def pyramidplot(data=None, var_levels=None, var_values=None, ax=None, cmap='viridis', label_levels=True, label_values=True, show_trend=False, trend_format='{:.1f}%', edgecolor='black', label_color=None, trend_color='gray', invert_trend=False):
    """
    Create a pyramid plot from a pandas DataFrame or two lists.

    Parameters:
    - data: pandas DataFrame or list-like, optional. 
        If DataFrame, provide `var_levels` and `var_values` as column names.
        If list-like, this is treated as the levels (categories), and `var_levels` should be the values list.
        If None, `var_levels` and `var_values` must be provided as lists.
    - var_levels: str or list-like, optional. 
        If data is DataFrame, this is the column name for levels.
        If data is list-like (as second arg), this is the list of values.
        If data is None, this must be the list of levels.
    - var_values: str or list-like, optional. 
        Column name for values (only used if data is DataFrame).
        If data is None, this must be the list of values.
    - ax: matplotlib Axes object, optional. If None, a new figure and axes are created.
    - cmap: str or Colormap, optional. Colormap to use for the levels.
    - label_levels: bool, optional. Whether to label the levels.
    - label_values: bool, optional. Whether to label the values.
    - show_trend: bool, optional. Whether to show trend arrows indicating change between levels.
    - trend_format: str, optional. Format string for the trend labels (default '{:.1f}%').
    - edgecolor: str or None, optional. Color of the polygon edges. Default is 'black'. Use 'none' or None to remove edges.
    - label_color: str or color-like or None, optional. Color for the level labels. If None, uses the same color as the level.
    - trend_color: str or color-like, optional. Color for the trend arrows and labels. Default is 'gray'.
    - invert_trend: bool, optional. If True, inverts the trend arrow direction (downwards) and sign of the percentage. Default is False.
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 6))
    
    if data is not None:
        if isinstance(data, pd.DataFrame):
            if var_levels is None or var_values is None:
                raise ValueError("When 'data' is a DataFrame, 'var_levels' and 'var_values' must be provided.")
            df = data.copy()
        elif isinstance(data, (list, np.ndarray, pd.Series)):
            # Assume data is levels, var_levels is values
            if var_levels is None:
                 raise ValueError("When 'data' is a list (levels), the second argument must be a list of values.")
            
            levels = data
            values = var_levels
            
            # Create internal DataFrame
            var_levels = "Level"
            var_values = "Value"
            df = pd.DataFrame({var_levels: levels, var_values: values})
        else:
            raise ValueError("Invalid input for 'data'. Provide a DataFrame or list-like.")
    else:
        # data is None, check if var_levels and var_values are lists
        if var_levels is not None and var_values is not None:
            if isinstance(var_levels, (list, np.ndarray, pd.Series)) and isinstance(var_values, (list, np.ndarray, pd.Series)):
                levels = var_levels
                values = var_values
                
                # Create internal DataFrame
                var_levels = "Level"
                var_values = "Value"
                df = pd.DataFrame({var_levels: levels, var_values: values})
            else:
                 raise ValueError("When 'data' is None, 'var_levels' and 'var_values' must be lists.")
        else:
            raise ValueError("Must provide 'data' or both 'var_levels' and 'var_values' as lists.")
    
    # Ensure values are numeric
    df[var_values] = pd.to_numeric(df[var_values], errors='coerce')
    
    n_levels = len(df)
    height = 1.0  # Height of each level
    
    max_val = df[var_values].max()
    
    # Color map
    colors = plt.get_cmap(cmap)(np.linspace(0, 1, n_levels))
    
    for i, row in df.iterrows():
        val = row[var_values]
        level_name = row[var_levels]
        
        # Y coordinates for this level
        y_bottom = i * height
        y_top = (i + 1) * height
        
        # Trapezoids connecting current value to next value
        # Bottom width = current value
        # Top width = next value (or 0 if last level)
        
        if i < n_levels - 1:
            next_val = df.iloc[i+1][var_values]
        else:
            next_val = 0 # Point at the top
            
        x_bottom_left = -val / 2
        x_bottom_right = val / 2
        x_top_left = -next_val / 2
        x_top_right = next_val / 2
        
        poly_points = [
            [x_bottom_left, y_bottom],
            [x_bottom_right, y_bottom],
            [x_top_right, y_top],
            [x_top_left, y_top]
        ]
        
        poly = Polygon(poly_points, closed=True, facecolor=colors[i], edgecolor=edgecolor)
        ax.add_patch(poly)
        
        # Labels
        # Define label x position
        # Center labels and arrows
        label_x = -max_val * 0.75 
        
        if label_levels:
            # Label centered
            # Determine color
            c = label_color if label_color is not None else colors[i]
            ax.text(label_x, (y_bottom + y_top)/2, level_name, 
                    ha='center', va='center', fontsize=10, fontweight='bold', color=c)
            
        if label_values:
            # Label in the center
            ax.text(0, (y_bottom + y_top)/2, str(val), 
                    ha='center', va='center', color='white' if np.mean(colors[i][:3]) < 0.5 else 'black', fontsize=10)

        # Trend Overlay
        if show_trend and i < n_levels - 1:
            # Arrows aligned with labels
            arrow_fixed_x = label_x 
            
            # Calculate percentage
            if val != 0:
                change_pct = (next_val - val) / val * 100
                if invert_trend:
                    change_pct = -change_pct
                txt = trend_format.format(change_pct)
            else:
                txt = ""

            # Draw arrow
            # Add padding to avoid overlapping with text
            # Assuming height is 1.0, text is at center.
            # Start a bit above the current center, end a bit below the next center.
            padding = height * 0.25
            y_center_current = (y_bottom + y_top)/2
            y_center_next = (y_top + y_top + height)/2
            
            y_start = y_center_current + padding
            y_end = y_center_next - padding
            
            if invert_trend:
                # Swap start and end to point downwards
                y_start, y_end = y_end, y_start
            
            # Smaller arrow
            style = "Simple, tail_width=0.3, head_width=3, head_length=6"
            kw = dict(arrowstyle=style, color=trend_color)
            
            # Arrow from level i to level i+1
            a = FancyArrowPatch((arrow_fixed_x, y_start), (arrow_fixed_x, y_end),
                                connectionstyle="arc3,rad=0.0", **kw) # Straight vertical arrow
            ax.add_patch(a)
            
            # Annotation
            # Text to the right of the arrow
            ax.text(arrow_fixed_x + max_val * 0.05, (y_center_current + y_center_next)/2, txt, 
                    ha='left', va='center', color=trend_color, fontsize=10)

    # Set limits and aspect
    # Adjust xlim to accommodate labels on the left
    ax.set_xlim(-max_val * 1.2, max_val * 0.8)
    ax.set_ylim(0, n_levels * height)
    ax.axis('off') # Hide axis
    
    return ax
