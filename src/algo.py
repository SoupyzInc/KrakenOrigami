import time
import asyncio
import krakenex
import logging
from ta import macd, convert
from paper import register, buy, close_algo#, valid
from datetime import datetime

run = True

def start():
    """ 
    Starts the trading algorithm.
    """

    global run
    run = True

def kill():
    """
    Kills the trading algorithm.
    """

    global run
    run = False

async def trade(base, quote):
    """
    The central processing of the trading algorithm. No techincal analysis is done here; only oversight of interpreting the TA.

    Args:

        base: The base to be traded
        quote: The quote to be traded
    """

    k = krakenex.API()
    id = 743348410303774801

    # if not valid(id): # Registers account for the bot
    #     register(id)

    global run
    position = False
    logging.basicConfig(filename='algo.log', encoding='utf-8', level=logging.DEBUG)

    while run:
        logging.debug(str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ' | ---------------------------NEW MINUTE---------------------------')
        pair = convert(base, quote)
        data = k.query_public('OHLC', {'pair': pair})['result'][pair] 
        # data = k.query_public('OHLC', {'pair': pair, 'interval': '1'})['result'][pair] # OHLC DATA [LOC][VALUE]
        logging.debug(str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ' | CALCULATING MACD')
        result = macd(data) # TA

        logging.debug(str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ' | MACD: ' + str(result))
        if result == 1: # ENTRY
            buy(id, pair, data[-1][4], 100)
            logging.debug(str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ' | BOUGHT ' + pair + ' | ' + data[-1][4])
            position = True
        elif result == 0 and position: # EXIT
            try:
                close_algo(id, 1)
                logging.debug(str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ' | CLOSED ' + pair + ' | ' + data[-1][4])
            except ValueError as err:
                logging.error(err)
            except UnboundLocalError as err:
                logging.error(err)
        
        await asyncio.sleep(10) # Wait 10 seconds for new data

### Debug
# def main():
#     trade('btc', 'usd')

# if __name__ == "__main__":
#     main()
###
