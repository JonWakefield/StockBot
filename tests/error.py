import yfinance as yf
import matplotlib.pyplot as plt

# change period to "1mo" if running on a friday to view error
data = yf.download("AAPL", period="5d", interval="1d")

# Extract the dates and close prices from the dataframe
dates = data.index.strftime('%Y-%m-%d')  # Convert datetime index to strings
close_prices = data["Close"]

print(type(dates))
print(type(close_prices))

# Plot the data as a bar plot with categorical variables
plt.plot(dates, close_prices)

plt.tick_params("both", labelsize=7)

plt.show()