import matplotlib.pyplot as plt
import numpy as np

# Create some data
x = np.linspace(0.1, 10, 10)  # Adjusted x values to avoid log(0)
y1 = np.sin(x)
y2 = np.exp(x)  # Exponential data for demonstration

# Create a figure and axis object
fig, ax1 = plt.subplots()

ax2 = ax1.twinx()
ax2.bar(x, y2, color='r')  # Setting zorder to 1 makes it appear in the background
# Plot the first dataset with the first y-axis
ax1.plot(x, y1, 'b-')  # Setting zorder to 2 makes it appear in the foreground
ax1.set_xlabel('X data')
ax1.set_ylabel('Y1 data', color='b')

ax1.set_facecolor('none')
ax2.set_zorder(1)
ax1.set_zorder(2.5)
# Create a second y-axis sharing the same x-axis

# Plot the second dataset with the second y-axis

# Set the scale of the second y-axis to logarithmic
ax2.set_yscale('log')
ax2.set_ylabel('Y2 data (log scale)', color='r')

# Add a title
plt.title('Matplotlib chart with two y-axes (log scale for Y2)')

# Show the plot
plt.show()
