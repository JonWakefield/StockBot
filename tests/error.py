import yfinance as yf
import matplotlib.pyplot as plt

# change period to "1mo" if running on a friday to view error
data = yf.download("AAPL", period="5d", interval="1d")

dates = data.index.strftime('%Y-%m-%d') 

print(type(data.index[0]))

plt.bar(dates, data["Close"])

plt.tick_params("both", labelsize=7)

plt.show()










