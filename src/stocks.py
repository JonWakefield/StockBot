# from ..cogs.finance import Finance
import matplotlib.pyplot as plt
import yfinance as yf
from utils.strings import Strings
from config.config import bot_settings, log
import numpy as np
import io
from PIL import Image

class Stocks():


    def __init__(self):
        pass

    
    async def get_ticker_info(ticker: str) -> dict:
        """"""
        yf_ticker = yf.Ticker(ticker)

        ticker_info = yf_ticker.info

        try:
            symbol = ticker_info["symbol"]
            fifty_week_low = ticker_info["fiftyTwoWeekLow"] 
            fifty_week_high = ticker_info["fiftyTwoWeekHigh"]
            fifty_day_avg = ticker_info["fiftyDayAverage"]
            short_ratio = ticker_info["shortRatio"]
            company_name = ticker_info["longName"]
            avg_volume = ticker_info["averageVolume"]
        except KeyError as e:
            return {"Status": f"Unable to retreive stock info for {ticker} (For Crypto, use !coin)"}
        
        # TODO: During market hours, See if theres any difference between rec_data_frame data and the recent data from yf_ticker 
        rec_data_frame = yf_ticker.history(period="1d")

        stock_data = {
            "Company": company_name,
            "Ticker": symbol,
            "High": round(rec_data_frame['High'].iloc[0], bot_settings.DECIMAL_PLACES),
            "Open": round(rec_data_frame['Open'].iloc[0], bot_settings.DECIMAL_PLACES),
            "Close": round(rec_data_frame['Close'].iloc[0], bot_settings.DECIMAL_PLACES),
            "Low": round(rec_data_frame['Low'].iloc[0], bot_settings.DECIMAL_PLACES),
            "Volume": Strings.add_commas(str(rec_data_frame['Volume'].iloc[0])),
            "Avg. Volume": Strings.add_commas(str(avg_volume)),
            "52 Week High": fifty_week_high, 
            "50 Day Avg.": fifty_day_avg,
            "Short Ratio": short_ratio,
            "52 Week Low": fifty_week_low, 
        }

        return stock_data




    async def create_line_chart(security: str,
                                time_frame: str,
                                interval: str,
                                y_axis: str) -> bytes:
        """
        """
        font = {
            'family': 'serif',
            'color': '#FFFDD0',
            'weight': 'bold',
            'size': 16,
        }

        color1 = "green"
        color2 = "red"

        stock_data = yf.download(tickers=security, 
                                 period=time_frame,
                                 interval=interval)
        
        # Calculate daily price change
        stock_data['Price Change'] = stock_data['Close'].diff()

        # Create the plot
        for i in range(1, len(stock_data)):
            if stock_data['Price Change'].iloc[i] >= 0:
                plt.plot([stock_data.index[i - 1], stock_data.index[i]], [stock_data['Close'].iloc[i - 1], stock_data['Close'].iloc[i]], color=color1)
            else:
                plt.plot([stock_data.index[i - 1], stock_data.index[i]], [stock_data['Close'].iloc[i - 1], stock_data['Close'].iloc[i]], color=color2)
                        

        # stock_data[y_axis].plot(color='#FFFDD0') # uncomment to go back to original
        if y_axis == "Volume": plt.title(f"${security.upper()} {time_frame.upper()} {y_axis}", fontdict=font)
        else: plt.title(f"${security.upper()} {time_frame.upper()} {y_axis} Prices", fontdict=font)


        # Set background color of the entire chart
        # plt.gcf().set_facecolor('#0c0a09')  # Use any color code or name you prefer
        plt.gcf().set_facecolor('#020617')  # Use any color code or name you prefer

        # Set background color of the plot area
        plt.gca().set_facecolor('#1B1B1B')  # Use any color code or name you prefer

        plt.xlabel('', fontdict=font)
        # plt.ylabel('$', fontdict=font)

        # Change the color of x and y-axis tick marks
        plt.tick_params(axis='x', 
                        colors='#FFFDD0',
                        labelsize=7)
        plt.tick_params(axis='y', 
                        colors='#FFFDD0',
                        labelsize=8)

        # Add grid lines
        plt.grid(color='gray', linestyle='--', linewidth=0.5)

        # create an in-memory binrary stream to store the file
        buf = io.BytesIO()
        # write the figure to the in-memory binary stream (instead of a file on disk)
        plt.savefig(buf, format='png')
        # move position back to the start of the file (so we read from the start)
        buf.seek(0)
        # close the plot
        plt.close()

        return buf
    

    async def create_candle_chart(security: str,
                                  time_frame: str,
                                  interval: str) -> bytes:
        
        color1 = "red"
        color2 = "green"
        width = 0.3
        width2 = 0.03

        font = {
            'family': 'serif',
            'color': '#FFFDD0',
            'weight': 'bold',
            'size': 16,
        }

        stock_data = yf.download(tickers=security, 
                                 period=time_frame,
                                 interval=interval)
        
        # setup data
        up = stock_data[stock_data['Close'] >= stock_data['Open']]
        down = stock_data[stock_data['Close'] < stock_data['Open']]

        # # Plotting up prices of the stock 
        plt.bar(up.index, up["Close"] - up["Open"], width, bottom=up["Open"], color=color1) 
        plt.bar(up.index, up["High"] - up["Close"], width2, bottom=up["Close"], color=color1) 
        plt.bar(up.index, up["Low"] - up["Open"], width2, bottom=up["Open"], color=color1) 

        # Plotting down prices of the stock 
        plt.bar(down.index, down["Close"] - down["Open"], width, bottom=down["Open"], color=color2) 
        plt.bar(down.index, down["High"] -  down["Open"], width2, bottom=down["Open"], color=color2) 
        plt.bar(down.index, down["Low"] - down["Close"], width2, bottom=down["Close"], color=color2) 

        # # rotating the x-axis tick labels at 30degree 
        # # towards right 
        plt.xticks(rotation=30, ha='right') 

        # custom the chart
        plt.title(f"${security.upper()} {time_frame.upper()} Candles", fontdict=font)
        plt.gcf().set_facecolor('#020617')
        plt.gca().set_facecolor('#1B1B1B')

        # Change the color of x and y-axis tick marks
        plt.tick_params(axis='x', colors='#FFFDD0')
        plt.tick_params(axis='y', colors='#FFFDD0')

        # Add grid lines
        plt.grid(color='gray', linestyle='--', linewidth=0.5)

        # # create an in-memory binrary stream to store the file
        buf = io.BytesIO()
        # # write the figure to the in-memory binary stream (instead of a file on disk)
        plt.savefig(buf, format='png')
        # # move position back to the start of the file (so we read from the start)
        buf.seek(0)
        # # close the plot
        plt.close()

        return buf

    async def create_area_chart(security: str,
                                time_frame: str,
                                interval: str,
                                y_axis: str) -> bytes:
        

        stock_data = yf.download(tickers=security, 
                                 period=time_frame,
                                 interval=interval)

        stock_data[y_axis].plot()

        plt.fill_between(stock_data.index, stock_data[y_axis], color="blue", alpha=0.6, label="Area 1")

        plt.ylim(160,200) #TODO: Need to find best way to set lower and upper bound y-limits

        plt.title(f"{security} Stock Prices")

        # create an in-memory binrary stream to store the file
        buf = io.BytesIO()
        # write the figure to the in-memory binary stream (instead of a file on disk)
        plt.savefig(buf, format='png')
        # move position back to the start of the file (so we read from the start)
        buf.seek(0)
        # close the plot
        plt.close()

        return buf
