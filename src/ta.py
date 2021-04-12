import krakenex
from pairs import bases, quotes, pair

def get_ohlcs(pair):
    """
    Gets 720, 1 hour candle sticks of OHLC data.

    Args:

        pair: The pair to be queried.

    Returns:

        A list containing a list of OHLC data in the format: time, open, high, low, close, vwap, volume, count
        Ex: get_ohlcs(pair)[<unix_time>][<value (0-7)>]
    """
    k = krakenex.API()
    # Load data for analysis
    return k.query_public('OHLC', {'pair': pair, 'interval': '60'})['result'][pair]

def get_ohlc(pair):
    """
    Gets the latest 1 hour candle stick of OHLC data.

    Args:

        pair: The pair to be queried.

    Returns:

        A list of the latest OHLC data in the format: time, open, high, low, close, vwap, volume, count
        Ex: get_ohlc(pair)[<value (0-7)>]
    """
    k = krakenex.API()
    # Load data for analysis
    return k.query_public('OHLC', {'pair': pair, 'interval': '60'})['result'][pair][-1]

def valid_pair(pairIn):
    """
    Validate that a pair is tradable on Kraken.

    Args:

        pairIn: The pair to be checked.

    Returns:

        Boolean True if the pair can be traded on Kraken and False if it cannot.
    """

    valid_pairs = pair.values()
    for valid_pair in valid_pairs:
        if valid_pair == pairIn:
            return True
    
    return False

def valid_base_quote(base, quote):
    """
    Validates that a base and quote can be converted into a Kraken API pair.

    Args:

        base: The base to be checked
        quote: The quote to be checked

    Returns:

        Boolean True if the base and quote can be converted into a Kraken API pair and false if not.
    """
    
    try:
        base = bases[base.upper()] # Convert human readable base to Kraken API base
    except: 
        return False
    else:
        try:
            quote = quotes[quote.upper()] # Convert human readable quote to readable quote
        except: 
            return False
        else:
            return True

def convert(base, quote):
    """
    Validates that a base and quote can be converted into a Kraken API pair.

    Args:

        base: The base to be converted
        quote: The quote to be converted

    Returns:

        The converted Kraken API pair as a string.

    Raises:

        base + " is not a valid base. Use `.pairs` to see a list of all valid pairs."
            If the readable base cannot be converted into a Kraken API formatted base.
        quote + " is not a valid quote. Use `.pairs` to see a list of all valid pairs."
            If the readable quote cannot be converted into a Kraken API formatted quote.
        base + quote + " is not a valid base/quote pair. Use `.pairs` to see a list of all valid pairs."
            If the readable base/quote pair cannot be converted into a Kraken API formatted pair.
    """

    try:
        base = bases[base.upper()] # Convert human readable base to Kraken API base
    except: 
        return base + " is not a valid base. Use `.pairs` to see a list of all valid pairs."
    else: # Valid base
        try:
            quote = quotes[quote.upper()] # Convert human readable quote to readable quote
        except: 
            return quote + " is not a valid quote. Use `.pairs` to see a list of all valid pairs."
        else: # Valid quote
            try:
                pair[base + quote]
            except:
                return base + quote + " is not a valid base/quote pair. Use `.pairs` to see a list of all valid pairs."
            else:
                return pair[base + quote]

def ema(period, value, data):
    """
    Returns the EMA of the given data for a given period.

    Args:

        period: The time period or interval, in minutes, to be used.
        value: Which value from the OHLC data to be averaged. Values are as follows:
          1 - time, 2 - open, 2 - high, 3 - low, 4 - close, 5 - vwap, 6 - volume, 7 - count
        data: The data set to be used. Expects the Kraken API's OHLC data array.
          Ex: data = k.query_public('OHLC', {'pair': XLTCZUSD, 'interval': '60'})['result'][XLTCZUSD] 
        
    Returns:

        An array of the exponential moving average.
    """

    k = 2 / (period + 1)
    EMA = []
    i = 1
    sum = 0
    while i < period:
        sum += float(data[-i][value])
        i += 1

    sum = sum / period
    EMA.append(sum)

    i = period + 1
    while i < len(data): # Calculate EMA
        EMA.append(float(data[i][value]) * k + float(EMA[i - (period + 1)]) * (1 - k))
        i += 1

    return EMA

def ema_list(period, data):
    """
    Returns the EMA of the given data for a given period.

    Args:

        period: The time period or interval, in minutes, to be used.
        data: The data set to be used. Expects a list.
        
    Returns:

        An array of the exponential moving average.
    """

    k = 2 / (period + 1)
    EMA = []
    i = 1
    sum = 0
    while i < period:
        sum += float(data[-i])
        i += 1

    sum = sum / period
    EMA.append(sum)

    i = period + 1
    while i < len(data): # Calculate EMA
        EMA.append(float(data[i]) * k + float(EMA[i - (period + 1)]) * (1 - k))
        i += 1

    return EMA

def ema_ta(data):
    """
    Returns technical analysis based on EMA clouds.

    Args:

        data: The Kraken OHLC data to be evaluated. Expects the Kraken API's OHLC data array.

    Returns:

        A string with the technical analysis.
    """

    # Below red cloud
    if float(data[-1][4]) < ema(40, 4, data)[-1]: 
            emaText = 'Possible entry point.'
    # In red cloud
    elif (float(data[-1][4]) >= ema(40, 4, data)[-1]) & (float(data[-1][4]) < ema(30, 4, data)[-1]):
        emaText = 'Possible entry point or close position.'
    # Between clouds
    elif (float(data[-1][4]) >= ema(30, 4, data)[-1]) & (float(data[-1][4]) < ema(20, 4, data)[-1]):
        emaText = 'Possible entry point or (prepare to) close position.' 
    # In green cloud
    elif (float(data[-1][4]) >= ema(20, 4, data)[-1]) & (float(data[-1][4]) < ema(10, 4, data)[-1]):
        emaText = 'Continue to hold.' 
    # Above green cloud
    else:
        emaText = 'Continue to hold or close position.'

    return emaText

def macd(data):
    """
    Does basic MACD technical analysis.

    Args:

        data: The Kraken OHLC data to be evaluated. Expects the Kraken API's OHLC data array.

    Returns:

        1 if the algorithm should buy, 0 if the algorithm should close a buy position, and -1 if no position can be determined.
    """

    ema_26 = ema(26, 4, data)
    ema_12 = ema(12, 4, data)
    MACD = []

    i = 0
    while i < len(ema_26):
        MACD.append(ema_12[i] - ema_26[i])
        i += 1
    
    signal = ema_list(9, MACD)

    histogram = []

    i = 1
    while (i <= len(MACD)) and (i <= len(signal)):
        histogram.append(MACD[-i] - signal[-i]) # Iterate backwards to "align" data forwards
        i += 1
    
    # Iterate backwards
    # POS -> NEG (ENTRY)
    # NEG -> POS (EXIT)

    if histogram[-1] > 0: # POS going into
        if histogram[-2] < 0: # NEG
            return 1 # ENTRY
        else:
            return -1
    elif histogram[-1] < 0: # NEG going into
        if histogram[-2] > 0: # POS
            return 0 # EXIT
        else:
            return -1
    else: # Wait for stronger signal
        return -1
