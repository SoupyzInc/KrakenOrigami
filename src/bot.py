import time
import pytz
import json
import logging
import krakenex
import discord
from discord.ext import commands
from datetime import datetime
from pairs import quotes, bases, pair, base_urls, base_colors

### NOTE: SMA CALCULATIONS ARE WRONG AND NEED TO BE FIXED. 
# CALCULATIONS ARE HIGHER THAN KRAKEN SMA. ###
def sma(period, value, data):
    """
    Return the SMA of the given data for a given period.

    Args:
        period: The time period or interval, in minutes, to be used.
        value: Which value from the OHLC data to be averaged. Values are as follows:
          1 - time, 2 - topen, 2 - high, 3 - low, 4 - close, 5 - vwap, 6 - volume, 7 - count
        data: The data set to be used. Expects the Kraken API's OHLC data array. 
          Ex: data = k.query_public('OHLC', {'pair': XLTCZUSD, 'interval': '60'})['result'][XLTCZUSD] 
        
    Returns:
        An array of the simple moving average.
    """

    loc = 0
    offset = 0

    sum = float(0)
    SMA = []

    while loc < len(data): # Iterate all values
        if loc == (period + offset):
            SMA.append(sum / period) 

            offset += 1
            loc = offset  
            sum = 0

            loc = loc - 1
        else:
            sum += float(data[loc][value]) # Sum closing values
            loc += 1

    return SMA

def main():
    """
    The main method that runs the Discord bot.
    """

    logger = logging.getLogger('discord')
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(name)s\n\t%(message)s'))
    logger.addHandler(handler)

    bot = commands.Bot(command_prefix='.')
    bot.remove_command("help")

    @bot.event
    async def on_ready():
        print('Logged in as {0.user}'.format(bot))

    ### HELP COMMANDS ### 
    @bot.command(name = 'help')
    async def documenatation(ctx, type = ''):
        if type == '':
            embed = discord.Embed(title = 'Kraken Origami Documentation', 
                            description = '`.help register`\n`.help info`', color = 0x5741d9)
        elif type == 'register':
            embed = discord.Embed(title = '.register Documentation', 
                            description = 'Registers an account to begin paper trading.', color = 0x5741d9)
        elif type == 'info':
            embed = discord.Embed(title = '.info Documentation',
                            description = '`.info <Base> <Quote>`\n Returns info from the Kraken API on' +
                            ' the specified pair.', color = 0x5741d9)
        
        embed.set_thumbnail(url = bot.user.avatar_url)
        embed.set_footer(text = 'Requested by ' + ctx.author.name + '.', icon_url = ctx.author.avatar_url)
        await ctx.send(embed = embed)

    ### ECONOMY COMMANDS ###
    @bot.command()
    async def register(ctx):
        data = {}
        data['people'] = []
        with open('data.txt') as json_file:
            data = json.load(json_file)

        for p in data['people']: #Prevent duplicate accounts
            if ctx.message.author.id == p['id']:
                await ctx.send('You have already ospened an account.')
                return

        data['people'].append({
            'id': ctx.message.author.id,
            'balance': '1000',
            'positions': {}
        })

        with open('data.txt', 'w') as outfile:
            json.dump(data, outfile)

        await ctx.send('Opened an account for ' + ctx.message.author.name + '.')

    @bot.command()
    async def info(ctx, base, quote):
        crypto = base.upper() + quote.upper() # Generate name
        base = bases[base.upper()] # Convert human readable base to Kraken API base
        quote = quotes[quote.upper()] # Convert human readable quote to readable quote
        
        k = krakenex.API()

        # Load data for analysis
        data = k.query_public('OHLC', {'pair': pair[base + quote], 'interval': '60'})['result'][pair[base + quote]] 
                                      # Get most recent price
        embed = discord.Embed(title = data[-1][4] + ' | ' + crypto, color = base_colors[base])
        embed.timestamp = datetime.utcnow().replace(tzinfo=pytz.utc)
        embed.add_field(name = 'SMA', value = '10 SMA | ' + str(round(sma(10, 4, data)[-1], 2)) +
                                            '\n20 SMA | ' + str(round(sma(20, 4, data)[-1], 2)) +
                                            '\n30 SMA | ' + str(round(sma(30, 4, data)[-1], 2)) +
                                            '\n40 SMA | ' + str(round(sma(40, 4, data)[-1], 2)))
        
        # Below red cloud
        if float(data[-1][4]) < sma(40, 4, data)[-1]: 
            ta = 'Possible entry point.'
        # In red cloud
        elif (float(data[-1][4]) >= sma(40, 4, data)[-1]) & (float(data[-1][4]) < sma(30, 4, data)[-1]):
            ta = 'Possible entry point or close position.'
        # Between clouds
        elif (float(data[-1][4]) >= sma(30, 4, data)[-1]) & (float(data[-1][4]) < sma(20, 4, data)[-1]):
            ta = 'Possible entry point or (prepare) to close position.' 
        # In green cloud
        elif (float(data[-1][4]) >= sma(20, 4, data)[-1]) & (float(data[-1][4]) < sma(10, 4, data)[-1]):
            ta = 'Continue to hold.' 
        # Above green cloud
        else:
            ta = 'Continue to hold or close position.'
        
        embed.add_field(name = 'TA', value = ta)
        embed.set_thumbnail(url = base_urls[base])

        await ctx.send(embed = embed)

    bot.run(open("token.txt", "r").read())

if __name__ == "__main__":
    main()
