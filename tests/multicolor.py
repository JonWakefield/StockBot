import yfinance as yf
import matplotlib.pyplot as plt

# Download stock data for Apple (AAPL)
stock_data = yf.download("AAPL", period="ytd", interval='1d')

# Calculate daily price change
stock_data['Price Change'] = stock_data['Close'].diff()

# Create the plot
fig, ax = plt.subplots()

# Iterate through data points and change line color based on price change
for i in range(1, len(stock_data)):
    if stock_data['Price Change'][i] > 0:
        ax.plot([stock_data.index[i - 1], stock_data.index[i]], [stock_data['Close'][i - 1], stock_data['Close'][i]], color='green')
    elif stock_data['Price Change'][i] < 0:
        ax.plot([stock_data.index[i - 1], stock_data.index[i]], [stock_data['Close'][i - 1], stock_data['Close'][i]], color='red')
    else:
        ax.plot([stock_data.index[i - 1], stock_data.index[i]], [stock_data['Close'][i - 1], stock_data['Close'][i]], color='black')

# Set background color of the entire figure
fig.set_facecolor('#f0f0f0')  # Use any color code or name you prefer

# Set background color of the plot area
ax.set_facecolor('#dcdcdc')  # Use any color code or name you prefer

# Add grid lines
ax.grid(color='gray', linestyle='--', linewidth=0.5)

# Add labels and title
plt.xlabel('Date', fontsize=14, color='blue')
plt.ylabel('Price', fontsize=14, color='blue')
plt.title('AAPL Stock Price with Changing Line Color', fontsize=16, color='green')

# Show plot
plt.show()
