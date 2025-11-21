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
fig, ax = plt.subplots(figsize=(8, 5))
pyramidplot(data, var_levels="Level", var_values="Value", ax=ax, show_trend=True, edgecolor='none', label_color=None, trend_color='gray')

plt.title("Pyramid Plot")
plt.savefig("demo_plot.png")
print("Plot saved to demo_plot.png")
