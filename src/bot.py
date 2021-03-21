import pytz
import logging
import krakenex
import discord
from discord.ext import commands
from datetime import datetime
from pairs import quotes, bases, pair, base_urls, base_colors
from ta import ema, ema_list, ema_ta, macd, valid_pair, valid_base_quote, convert, get_ohlc
from paper import register, valid, get_balance, get_positions, buy, close

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
    bot.remove_command('help')

    @bot.event
    async def on_ready():
        print('Logged in as {0.user}'.format(bot))

    ### HELP COMMANDS ### 
    @bot.command(name = 'help')
    async def documenatation(ctx, type = ''):
        if type == 'register':
            embed = discord.Embed(title = '.register Documentation', 
                            description = '`.register`\n Registers an account to begin paper trading.', color = 0x5741d9)
        elif type == 'info':
            embed = discord.Embed(title = '.info Documentation',
                            description = '`.info <Base> <Quote>`\n Returns info from the Kraken API on the specified pair.', color = 0x5741d9)
        elif type == 'pairs':
            embed = discord.Embed(title = '.pairs Documentation',
                            description = '`.pairs`\n Returns all possible pairs in two messages.', color = 0x5741d9)
        elif type == 'account':
            embed = discord.Embed(title = '.account Documentation',
                            description = '`.account (@User)`\n Returns your account or the pinged user\'s account.', color = 0x5741d9)
        elif type == 'buy':
            embed = discord.Embed(title = '.buy Documentation',
                            description = '`.buy <Base> <Quote> <Amount>`\n Buys <Amount> in dollars of the specified pair.', color = 0x5741d9)
        elif type == 'close':
            embed = discord.Embed(title = '.close Documentation',
                            description = '`.close <Position #>`\n Closes your position. Position numbers are listed when you use `.account`', color = 0x5741d9)
        else:
            embed = discord.Embed(title = 'Kraken Origami Documentation', 
                            description = '`()` are optional parameters and `<>` are required parameters.\n\n`.help register`\n`.help info`\n`.help pairs`\n`.help account`\n`.help buy`\n`.help close`', color = 0x5741d9)

        embed.set_thumbnail(url = bot.user.avatar_url)
        embed.set_footer(text = 'Requested by ' + ctx.author.name + '.', icon_url = ctx.author.avatar_url)
        await ctx.send(embed = embed)

    @bot.command(name = 'pairs')
    async def _pairs(ctx):
        embed = discord.Embed(title = 'Pairs | 1/2', color = 0x5741d9,
                        description = 'AAVEAUD, AAVEETH, AAVEEUR, AAVEGBP, AAVEUSD, AAVEXBT, ADAAUD, ADAETH, ADAEUR, ADAGBP, ADAUSD, ADAUSDT, ADAXBT, ALGOETH, ALGOEUR, ALGOGBP, ALGOUSD, ALGOXBT, ANTETH, ANTEUR, ANTUSD, ANTXBT, ATOMAUD, ATOMETH, ATOMEUR, ATOMGBP, ATOMUSD, ATOMXBT, BALETH, BALEUR, BALUSD, BALXBT, BATETH, BATEUR, BATUSD, BATXBT, BCHAUD, BCHETH, BCHEUR, BCHGBP, BCHJPY, BCHUSD, BCHUSDT, BCHXBT, COMPETH, COMPEUR, COMPUSD, COMPXBT, CRVETH, CRVEUR, CRVUSD, CRVXBT, DAIEUR, DAIUSD, DAIUSDT, DASHEUR, DASHUSD, DASHXBT, DOTAUD, DOTETH, DOTEUR, DOTGBP, DOTUSD, DOTUSDT, DOTXBT, EOSETH, EOSEUR, EOSUSD, EOSUSDT, EOSXBT, ETHAUD, ETHCHF, ETHDAI, ETHUSDC, ETHUSDT, EURAUD, EURCAD, EURCHF, EURGBP, EURJPY, EWTEUR, EWTGBP, EWTUSD, EWTXBT, FILAUD, FILETH, FILEUR, FILGBP, FILUSD, FILXBT, FLOWETH, FLOWEUR, FLOWGBP, FLOWUSD, FLOWXBT, GNOETH, GNOEUR, GNOUSD, GNOXBT, GRTAUD, GRTETH, GRTEUR, GRTGBP, GRTUSD, GRTXBT, ICXETH, ICXEUR, ICXUSD, ICXXBT, KAVAETH, KAVAEUR, KAVAUSD, KAVAXBT, KEEPETH, KEEPEUR, KEEPUSD, KEEPXBT, KNCETH, KNCEUR, KNCUSD, KNCXBT, KSMAUD, KSMETH, KSMEUR, KSMGBP, KSMUSD, KSMXBT, LINKAUD, LINKETH, LINKEUR, LINKGBP, LINKUSD, LINKUSDT, LINKXBT, LSKETH, LSKEUR, LSKUSD, LSKXBT, LTCAUD, LTCETH, LTCGBP, LTCUSDT, MANAETH, MANAEUR, MANAUSD,')
        embed.set_thumbnail(url = bot.user.avatar_url)
        embed.set_footer(text = 'Requested by ' + ctx.author.name + '.', icon_url = ctx.author.avatar_url)
        await ctx.send(embed = embed)

        embed = discord.Embed(title = 'Pairs | 2/2', color = 0x5741d9,
                        description = 'MANAXBT, NANOETH, NANOEUR, NANOUSD, NANOXBT, OCEANEUR, OCEANGBP, OCEANUSD, OCEANXBT, OMGETH, OMGEUR, OMGUSD, OMGXBT, OXTETH, OXTEUR, OXTUSD, OXTXBT, PAXGETH, PAXGEUR, PAXGUSD, PAXGXBT, QTUMETH, QTUMEUR, QTUMUSD, QTUMXBT, REPVETH, REPVEUR, REPVUSD, REPVXBT, SCETH, SCEUR, SCUSD, SCXBT, SNXAUD, SNXETH, SNXEUR, SNXGBP, SNXUSD, SNXXBT, STORJETH, STORJEUR, STORJUSD, STORJXBT, TBTCETH, TBTCEUR, TBTCUSD, TBTCXBT, TRXETH, TRXEUR, TRXUSD, TRXXBT, UNIETH, UNIEUR, UNIUSD, UNIXBT, USDCAUD, USDCEUR, USDCGBP, USDCHF, USDCUSD, USDCUSDT, USDTAUD, USDTCAD, USDTCHF, USDTEUR, USDTGBP, USDTJPY, USDTUSD, WAVESETH, WAVESEUR, WAVESUSD, WAVESXBT, XBTAUD, XBTCHF, XBTDAI, XBTUSDC, XBTUSDT, XDGEUR, XDGUSD, XETCETH, XETCXBT, XETCEUR, XETCUSD, XETHXBT, XETHCAD, XETHEUR, XETHGBP, XETHJPY, XETHUSD, XLTCXBT, XLTCEUR, XLTCJPY, XLTCUSD, XMLNETH, XMLNXBT, XMLNEUR, XMLNUSD, XREPETH, XREPXBT, XREPEUR, XREPUSD, XRPAUD, XRPETH, XRPGBP, XRPUSDT, XTZAUD, XTZETH, XTZEUR, XTZGBP, XTZUSD, XTZXBT, XXBTCAD, XXBTEUR, XXBTGBP, XXBTJPY, XXBTUSD, XXDGXBT, XXLMXBT, XXLMAUD, XXLMEUR, XXLMGBP, XXLMUSD, XXMRXBT, XXMREUR, XXMRUSD, XXRPXBT, XXRPCAD, XXRPEUR, XXRPJPY, XXRPUSD, XZECXBT, XZECEUR, XZECUSD, YFIAUD, YFIETH, YFIEUR, YFIGBP, YFIUSD, YFIXBT')
        embed.set_thumbnail(url = bot.user.avatar_url)
        embed.set_footer(text = 'Requested by ' + ctx.author.name + '.', icon_url = ctx.author.avatar_url)     
        await ctx.send(embed = embed)

    ### ECONOMY COMMANDS ###
    @bot.command(name = 'register')
    async def _register(ctx):
        if valid(ctx.author.id):
            await ctx.send("Account already created. Use `.account` to view your account")
        else:
            try: 
                register(ctx.author.id)
            except: # Handle unexpected errors
                await ctx.send("Unknown Error: Account registration unsuccessful. Please try again.")
            else:
                await ctx.send("Account registered successfully. You now have a balance of 1,000 USD. Happy trading!")
  
    @bot.command(name = 'account')
    async def _account(ctx, *, member: discord.Member=None):
        if member is None: # No user pinged
            member = ctx.author

        if (valid(member.id)): # Check if user has an account
            embed = discord.Embed(title = member.display_name + "'s Accounts", color = 0x5741d9)
            embed.timestamp = datetime.utcnow().replace(tzinfo=pytz.utc)

            embed.add_field(name = 'Balance', value = "${:,.3f}".format(get_balance(member.id)))
            embed.add_field(name = 'All Time', value = "Coming Soon:tm:")
            embed.add_field(name = 'Monthly', value = "Coming Soon:tm:")

            positions = get_positions(member.id)  

            if len(positions) > 0:
                out = ""

                i = 1 # Track position number
                for position in positions:
                    price = float(get_ohlc(position[2])[4]) # Get current price
                    percent_gain = ((price - position[4])/ position[4]) * 100 # Calculate %gain/loss
                    shares = position[5] / position[4] # Calculate shares of coin purchased
                    numerical_gain = (shares * price) - (shares * position[4]) # Calculate numerical gain/loss

                    # Format negative and positive symbols on embed
                    if (percent_gain > 0):
                        percent = "+" + str(round(percent_gain, 2)) + "%"
                        numerical = "+" + "${:,.3f}".format(numerical_gain)
                    elif (percent_gain < 0):
                        percent = str(round(percent_gain, 2)) + "%"
                        numerical_gain *= -1
                        numerical = "-" + "${:,.3f}".format(numerical_gain)
                    else:
                        percent = str(round(percent_gain, 2)) + "%"
                        numerical = "${:,.3f}".format(numerical_gain)
                    
                    out += "\n**" + str(i) + ". " + position[2] + "** | " + "${:,.3f}".format(price)
                    out += "\n> `" + percent + "` " + numerical + "\n> ${:,.3f}".format(position[5]) + " @ " + "${:,.3f}".format(position[4])
                    i += 1
                    
                embed.add_field(name = 'Positions', value = out)
            else:
                embed.add_field(name = 'Positions', value = "No positions open")

            embed.set_thumbnail(url = member.avatar_url)
            await ctx.send(embed = embed)
        else:
            await ctx.send(member.display_name + " does not yet have an account. Use `.register` to make an account to begin paper trading.")

    @bot.command(name = 'buy')
    async def _buy(ctx, base, quote, amount):
        if (valid(ctx.author.id)): # Check if user has an account to trade with.
            if (valid_base_quote(base, quote)): # Check if the base-quote-pair can be traded.
                if float(amount) > 0: # Check if amount is greater than 0
                    if (float(amount) <= get_balance(ctx.author.id)): # Check if user has enough balance to complete the transaction
                        k = krakenex.API()
                        data = k.query_public('OHLC', {'pair': convert(base, quote), 'interval': '60'})['result'][convert(base, quote)] 

                        try:
                            buy(ctx.author.id, convert(base, quote), float(data[-1][4]), float(amount))
                        except: # Handle unexpected errors
                            await ctx.send("Unknown error: Buy order unsuccessful. Please try again.")
                        else:
                            await ctx.send("Buy order `" + convert(base, quote) + " | " + "${:,.3f}".format(float(amount)) + " @ " + "${:,.3f}".format(float(data[-1][4])) + "` successfully filled.")
                    else:
                        await ctx.send("Balance of " + str("${:,.3f}".format(get_balance(ctx.author.id))) + " is insufficient for amount " + "${:,.3f}".format(float(amount))) # Not enough balance
                else:
                    await ctx.send("You must buy more than $0 of a coin.")
            else:
                await ctx.send(convert(base, quote)) # Base or quote not valid; uses the convert() error message
        else:
            await ctx.send("Register an account using `.register` to begin paper trading.") # Need an account

    @bot.command(name = 'close')
    async def _close(ctx, id):
        msg = close(ctx.author.id, id, ctx)

        if type(msg) is str: # Error message
            await ctx.send(msg)
        else:
            await ctx.send(embed = msg)
    
    @bot.command(name = 'info')
    async def _info(ctx, base, quote):
        crypto = base.upper() + quote.upper() # Generate name

        k = krakenex.API()

        # Load data for analysis
        data = k.query_public('OHLC', {'pair': convert(base, quote), 'interval': '60'})['result'][convert(base, quote)] 

        embed = discord.Embed(title = data[-1][4] + ' | ' + crypto, color = base_colors[base])
        embed.timestamp = datetime.utcnow().replace(tzinfo=pytz.utc)

        embed.set_footer(text = 'Requested by ' + ctx.author.name, icon_url = ctx.author.avatar_url) 
        embed.add_field(name = 'TA', value = ema_ta(data) + '\n' + macd(data))
        embed.set_thumbnail(url = base_urls[base])

        await ctx.send(embed = embed)

    bot.run(open("token.txt", "r").read())

if __name__ == "__main__":
    main()
