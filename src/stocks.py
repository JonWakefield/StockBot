import matplotlib.pyplot as plt
import yfinance as yf
from utils.strings import Strings
from config.config import bot_settings, log
import io

class Stocks():

    
    async def get_ticker_info(ticker: str) -> dict:
        """"""

        yf_ticker = yf.Ticker(ticker)

        ticker_info = yf_ticker.info

        try:
            if ticker_info["quoteType"] != "EQUITY":
                log.info(f"Wrong equity type submitted {ticker}")
                return {"Status": f"Unable to retreive stock info for {ticker} (For Crypto, use !coin. For ETF, use !etf)"}
        except KeyError as e:
            log.info(f"Unknown equity submitted {ticker}")
            return {"Status": f"Unable to retreive stock info for {ticker} (For Crypto, use !coin. For ETF, use !etf)"}

        try:
            stock_data = {
                "Company": ticker_info["longName"],
                "Ticker": ticker_info["symbol"],
                "High": ticker_info['dayHigh'],
                "Open": ticker_info['open'],
                "Close": ticker_info['previousClose'],
                "Low": ticker_info['dayLow'],
                "Volume": Strings.add_commas(str(ticker_info['volume'])),
                "Avg. Volume": Strings.add_commas(str(ticker_info["averageVolume"])),
                "52 Week High": ticker_info["fiftyTwoWeekHigh"], 
                "50 Day Avg.": ticker_info["fiftyDayAverage"],
                "Short Ratio": ticker_info["shortRatio"],
                "52 Week Low": ticker_info["fiftyTwoWeekLow"], 
            }
            return stock_data
        except KeyError as e:
            log.info(f"Got error trying to retreive key info for ticker {ticker}. Error {e}")
            return {"Status": f"Unable to retreive stock info for {ticker} (For coins, use !coin. For ETFs, use !etf)"}


    async def get_coin_info(coin: str) -> dict:
        """"""

        yf_ticker = yf.Ticker(coin)


        ticker_info = yf_ticker.info

        try:
            if ticker_info["quoteType"] != "CRYPTOCURRENCY":
                log.info(f"Wrong equity type submitted {coin}")
                return {"Status": f"Unable to retreive coin info for {coin} (For Stocks, use !ticker. For ETFs, use !etf)"}
        except KeyError as e:
            log.info(f"Unknown coin submitted {coin}")
            return {"Status": f"Unable to retreive coin info for {coin} (For Stocks, use !ticker. For ETFs, use !etf)"}
            
        try:
            coin_data = {
                "Market": ticker_info["lastMarket"],
                "Ticker": ticker_info["fromCurrency"],
                "High": ticker_info["dayHigh"],
                "Open": ticker_info["open"],
                "Close": ticker_info["previousClose"],
                "Low": ticker_info["dayLow"],
                "Volume": Strings.add_commas(str(ticker_info['volume'])),
                "Avg. Volume": Strings.add_commas(str(ticker_info["averageVolume"])),
                "52 Week High": ticker_info["fiftyTwoWeekHigh"], 
                "50 Day Avg.": ticker_info["fiftyDayAverage"],
                "52 Week Low": ticker_info["fiftyTwoWeekLow"], 
            }
            return coin_data
        except KeyError as e:
            log.info(f"Got error trying to retreive key info for ticker {coin}. Error {e}")
            return {"Status": f"Unable to retreive coin info for {coin} (For Stocks, use !ticker. For ETFs, use !etf)"}




    async def get_etf_info(ticker: str) -> dict:
        """"""

        yf_ticker = yf.Ticker(ticker)

        ticker_info = yf_ticker.info

        try:
            if ticker_info['quoteType'] != "ETF":
                log.info(f"Wrong equity type submitted {ticker}")
                return {"Status": f"Unable to retreive stock info for {ticker} (For Crypto, use !coin. For ETF, use !etf)"}
        except KeyError as e:
            log.info(f"Unknown etf submitted {ticker}")
            return {"Status": f"Unable to retreive stock info for {ticker} (For Crypto, use !coin. For ETF, use !etf)"}

        try:
            stock_data = {
                "Ticker": ticker_info["symbol"],
                "High": ticker_info['dayHigh'],
                "Open": ticker_info['open'],
                "Close": ticker_info['previousClose'],
                "Low": ticker_info['dayLow'],
                "Volume": Strings.add_commas(str(ticker_info['volume'])),
                "Avg. Volume": Strings.add_commas(str(ticker_info["averageVolume"])),
                "52 Week High": ticker_info["fiftyTwoWeekHigh"], 
                "50 Day Avg.": ticker_info["fiftyDayAverage"],
                "52 Week Low": ticker_info["fiftyTwoWeekLow"], 
            }
            return stock_data
        except KeyError as e:
            log.info(f"Got error trying to retreive key info for ticker {ticker}. Error {e}")
            return {"Status": f"Unable to retreive ETF info for {ticker} (For Stocks, use !ticker. For coins, use !coin)"}
        


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

        # NOTE: Bandaid fix to matplotlibs bullshit imaginary date problem
        dates = stock_data.index.strftime('%Y-%m-%d')  # Convert datetime index to strings
        close_prices = stock_data["Close"]
        ax2 = ax1.twinx()
        ax2.bar(dates, 
                stock_data['Volume'], 
                alpha=0.25, 
                color=bot_settings.VOLUME_COLOR)


        # Create the plot
        for i in range(1, len(stock_data)):
            if stock_data['Price Change'].iloc[i] >= 0:
                ax1.plot([dates[i - 1], dates[i]], [close_prices.iloc[i - 1], close_prices.iloc[i]], color=bot_settings.GREEN_COLOR)
            else:
                ax1.plot([dates[i - 1], dates[i]], [close_prices.iloc[i - 1], close_prices.iloc[i]], color=bot_settings.RED_COLOR)
                        

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

        ax1.set_xticks(dates[::15])

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
