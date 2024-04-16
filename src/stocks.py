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
            #TODO :
            3) Add ability to set what gets plotted (closing price, volume, etc.)
            4) add ability to do different chart types (line, area, candle, etc.)
            5) Add ability for multiple stocks
        
        """
        font = {
            'family': 'serif',
            'color': 'darkred',
            'weight': 'bold',
            'size': 16,
        }

        stock_data = yf.download(tickers=security, 
                                 period=time_frame,
                                 interval=interval)
        
        stock_data[y_axis].plot(color='peachpuff')
        if y_axis == "Volume": plt.title(f"${security.upper()} {time_frame.upper()} {y_axis}", fontdict=font)
        else: plt.title(f"${security.upper()} {time_frame.upper()} {y_axis} Prices", fontdict=font)


        # Set background color of the entire chart
        plt.gcf().set_facecolor('#0c0a09')  # Use any color code or name you prefer

        # Set background color of the plot area
        plt.gca().set_facecolor('#020617')  # Use any color code or name you prefer
        # plt.gca().set_facecolor('#0c0a09')  # Use any color code or name you prefer

        plt.xlabel('X-axis', fontdict=font)
        plt.ylabel('Y-axis', fontdict=font)

        # Change the color of x and y-axis tick marks
        plt.tick_params(axis='x', colors='darkred')
        plt.tick_params(axis='y', colors='darkred')

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

        stock_data = yf.download(tickers=security, 
                                 period=time_frame,
                                 interval=interval)

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
