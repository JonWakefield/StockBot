import matplotlib.pyplot as plt
import yfinance as yf
from utils.strings import Strings
from config.config import bot_settings, log
import io

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
                                interval: str) -> bytes:
        """
        """

        stock_data = yf.download(tickers=security, 
                                 period=time_frame,
                                 interval=interval)
        
        # Calculate daily price change
        stock_data['Price Change'] = stock_data['Close'].diff()

        fig, ax1 = plt.subplots()

        ax2 = ax1.twinx()
        ax2.bar(stock_data.index, 
                stock_data['Volume'], 
                alpha=0.25, 
                color=bot_settings.VOLUME_COLOR)

        # Create the plot
        for i in range(1, len(stock_data)):
            if stock_data['Price Change'].iloc[i] >= 0:
                ax1.plot([stock_data.index[i - 1], stock_data.index[i]], [stock_data['Close'].iloc[i - 1], stock_data['Close'].iloc[i]], color=bot_settings.GREEN_COLOR)
            else:
                ax1.plot([stock_data.index[i - 1], stock_data.index[i]], [stock_data['Close'].iloc[i - 1], stock_data['Close'].iloc[i]], color=bot_settings.RED_COLOR)
                        

        plt.title(f"${security.upper()} {time_frame.upper()}", fontdict=bot_settings.FONT_DICT)


        # Set background color of the entire chart
        fig.set_facecolor(bot_settings.BACKGROUND_COLOR) 
        # Set background color of the plot area
        ax1.set_facecolor('none') # ensure the bar chart can be seen

        # change z-order so bar chart is behind line
        ax2.set_zorder(1)
        ax1.set_zorder(2.5)

        plt.xlabel('', fontdict=bot_settings.FONT_DICT)

        # Change the color of x and y-axis tick marks
        ax1.tick_params(colors=bot_settings.WHITE_COLOR,
                        labelsize=7)
        ax2.tick_params(axis='y', 
                        which='both', 
                        colors=bot_settings.WHITE_COLOR, 
                        labelsize=7)

        # Add grid lines
        ax1.grid(color=bot_settings.WHITE_COLOR, 
                 linestyle='--', 
                 linewidth=0.5)

        ax2.set_yscale('log')

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
        
        stock_data = yf.download(tickers=security, 
                                 period=time_frame,
                                 interval=interval)
        

        fig, ax1 = plt.subplots()
        ax2 = ax1.twinx()

        ax2.bar(stock_data.index,
                stock_data['Volume'],
                alpha=0.25,
                color=bot_settings.VOLUME_COLOR)
        
        # setup data
        up = stock_data[stock_data['Close'] >= stock_data['Open']]
        down = stock_data[stock_data['Close'] < stock_data['Open']]

        # # Plotting up prices of the stock 
        ax1.bar(up.index, up["Close"] - up["Open"], bot_settings.CANDLE_WIDTH, bottom=up["Open"], color=bot_settings.GREEN_COLOR) 
        ax1.bar(up.index, up["High"] - up["Close"], bot_settings.STEM_WIDTH, bottom=up["Close"], color=bot_settings.GREEN_COLOR) 
        ax1.bar(up.index, up["Low"] - up["Open"], bot_settings.STEM_WIDTH, bottom=up["Open"], color=bot_settings.GREEN_COLOR) 

        # Plotting down prices of the stock 
        ax1.bar(down.index, down["Close"] - down["Open"],  bot_settings.CANDLE_WIDTH, bottom=down["Open"], color=bot_settings.RED_COLOR) 
        ax1.bar(down.index, down["High"] -  down["Open"], bot_settings.STEM_WIDTH, bottom=down["Open"], color=bot_settings.RED_COLOR) 
        ax1.bar(down.index, down["Low"] - down["Close"], bot_settings.STEM_WIDTH, bottom=down["Close"], color=bot_settings.RED_COLOR) 

        # # rotating the x-axis tick labels at 30degree 
        plt.xticks(rotation=30, ha='right') 

        # custom the chart
        plt.title(f"${security.upper()} {time_frame.upper()}", fontdict=bot_settings.FONT_DICT)

        fig.set_facecolor(bot_settings.BACKGROUND_COLOR)
        ax1.set_facecolor('none')

        ax2.set_zorder(1)
        ax1.set_zorder(2.5)

        ax1.tick_params(colors=bot_settings.WHITE_COLOR,
                        labelsize=7)
        
        ax2.tick_params(colors=bot_settings.WHITE_COLOR,
                        axis='y',
                        which='both',
                        labelsize=7)
        
        ax1.grid(color=bot_settings.WHITE_COLOR, 
                 linestyle='--', 
                 linewidth=0.5)

        ax2.set_yscale('log')

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
                                interval: str) -> bytes:
        

        stock_data = yf.download(tickers=security, 
                                 period=time_frame,
                                 interval=interval)
        
        fig, ax1 = plt.subplots()

        ax2 = ax1.twinx()

        ax2.bar(stock_data.index, 
                stock_data['Volume'], 
                alpha=0.25, 
                color=bot_settings.VOLUME_COLOR)

        # stock_data["Close"].plot()
        ax1.plot(stock_data["Close"])

        plt.fill_between(stock_data.index, stock_data["Close"], color="blue", alpha=0.6, label="Area 1")

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
