import krakenex

def ema(period, value, data):
    """
    Returns the EMA of the given data for a given period.

    Args:
        period: The time period or interval, in minutes, to be used.
        value: Which value from the OHLC data to be averaged. Values are as follows:
          1 - time, 2 - topen, 2 - high, 3 - low, 4 - close, 5 - vwap, 6 - volume, 7 - count
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

# WIP
def macd(data):
    ema_26 = ema(26, 4, data)
    ema_12 = ema(12, 4, data)
    MACD = []

    i = 0
    while i < len(ema_26):
        MACD.append(ema_12[i] - ema_26[i])
        i += 1
    
    signal = ema_list(9, MACD)

    # return (MACD, signal)

    # TA
    histogram = []

    i = 0 
    while (i < len(MACD)) & (i < len(signal)):
        histogram.append(MACD[i] - signal[i])
        i += 1
    
    # print(histogram)

    i = 1
    if MACD[-i] > signal[-i]: # Green; going to reverse to dip
        duration = 0 # How long the trend held
        max = 0
        max_loc = 0
        while MACD[-i] > signal[-i]: # Keep going back until trend reverses
            duration += 1
            if histogram[-i] > max:
                max = histogram[-i]
                max_loc = duration
            i += 1
        out = 'Movement duration: ' + str(duration) + '\nMax of ' + str(max) + ' at ' + str(max_loc) + '.'
    elif MACD[-i] < signal[-i]: # Red; going to reverse to growth
        duration = 0 # How long the trend held
        min = 0
        min_loc = 0
        while MACD[-i] > signal[-i]: # Keep going back until trend reverses
            duration += 1
            if histogram[-i] > min:
                min = histogram[-i]
                min_loc = duration
            i += 1
        out = 'Movement duration: ' + str(duration) + '\nMin of ' + str(min) + ' at ' + str(min_loc) + '.'
    else: # MACD = Signal; Go forward one period
        i = 2
        if MACD[-i] > signal[-i]: # Green; going to reverse to dip
            duration = 0 # How long the trend held
            max = 0
            max_loc = 0
            while MACD[-i] > signal[-i]: # Keep going back until trend reverses
                duration += 1
                if histogram[-i] > max:
                    max = histogram[-i]
                    max_loc = duration
                i += 1
            out = 'Movement duration: ' + str(duration) + '\nMax of ' + str(max) + ' at ' + str(max_loc) + '.'
        else: # Red; going to reverse to growth (Assume red if MACD still = Signal)
            duration = 0 # How long the trend held
            min = 0
            min_loc = 0
            while MACD[-i] > signal[-i]: # Keep going back until trend reverses
                duration += 1
                if histogram[-i] > min:
                    min = histogram[-i]
                    min_loc = duration
                i += 1
            out = 'Movement duration: ' + str(duration) + '\nMin of ' + str(min) + ' at ' + str(min_loc) + '.'

    return out
