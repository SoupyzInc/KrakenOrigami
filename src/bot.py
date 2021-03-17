import pytz
import logging
import krakenex
import discord
from discord.ext import commands
from datetime import datetime
from pairs import quotes, bases, pair, base_urls, base_colors
from ta import ema, ema_list, ema_ta, macd

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
        if type == 'register':
            embed = discord.Embed(title = '.register Documentation', 
                            description = '`.register`\n Registers an account to begin paper trading.', color = 0x5741d9)
        elif type == 'info':
            embed = discord.Embed(title = '.info Documentation',
                            description = '`.info <Base> <Quote>`\n Returns info from the Kraken API on the specified pair.', color = 0x5741d9)
        elif type == 'pairs':
            embed = discord.Embed(title = '.pairs Documentation',
                            description = '`.pairs`\n Returns all possible pairs in two messages.', color = 0x5741d9)
        else:
            embed = discord.Embed(title = 'Kraken Origami Documentation', 
                            description = '`.help register`\n`.help info`\n`.help pairs`', color = 0x5741d9)

        embed.set_thumbnail(url = bot.user.avatar_url)
        embed.set_footer(text = 'Requested by ' + ctx.author.name + '.', icon_url = ctx.author.avatar_url)
        await ctx.send(embed = embed)

    @bot.command(name = 'pairs')
    async def _pairs(ctx):
        embed = discord.Embed(title = 'Pairs 1/2', color = 0x5741d9,
                        description = 'AAVEAUD, AAVEETH, AAVEEUR, AAVEGBP, AAVEUSD, AAVEXBT, ADAAUD, ADAETH, ADAEUR, ADAGBP, ADAUSD, ADAUSDT, ADAXBT, ALGOETH, ALGOEUR, ALGOGBP, ALGOUSD, ALGOXBT, ANTETH, ANTEUR, ANTUSD, ANTXBT, ATOMAUD, ATOMETH, ATOMEUR, ATOMGBP, ATOMUSD, ATOMXBT, BALETH, BALEUR, BALUSD, BALXBT, BATETH, BATEUR, BATUSD, BATXBT, BCHAUD, BCHETH, BCHEUR, BCHGBP, BCHJPY, BCHUSD, BCHUSDT, BCHXBT, COMPETH, COMPEUR, COMPUSD, COMPXBT, CRVETH, CRVEUR, CRVUSD, CRVXBT, DAIEUR, DAIUSD, DAIUSDT, DASHEUR, DASHUSD, DASHXBT, DOTAUD, DOTETH, DOTEUR, DOTGBP, DOTUSD, DOTUSDT, DOTXBT, EOSETH, EOSEUR, EOSUSD, EOSUSDT, EOSXBT, ETHAUD, ETHCHF, ETHDAI, ETHUSDC, ETHUSDT, EURAUD, EURCAD, EURCHF, EURGBP, EURJPY, EWTEUR, EWTGBP, EWTUSD, EWTXBT, FILAUD, FILETH, FILEUR, FILGBP, FILUSD, FILXBT, FLOWETH, FLOWEUR, FLOWGBP, FLOWUSD, FLOWXBT, GNOETH, GNOEUR, GNOUSD, GNOXBT, GRTAUD, GRTETH, GRTEUR, GRTGBP, GRTUSD, GRTXBT, ICXETH, ICXEUR, ICXUSD, ICXXBT, KAVAETH, KAVAEUR, KAVAUSD, KAVAXBT, KEEPETH, KEEPEUR, KEEPUSD, KEEPXBT, KNCETH, KNCEUR, KNCUSD, KNCXBT, KSMAUD, KSMETH, KSMEUR, KSMGBP, KSMUSD, KSMXBT, LINKAUD, LINKETH, LINKEUR, LINKGBP, LINKUSD, LINKUSDT, LINKXBT, LSKETH, LSKEUR, LSKUSD, LSKXBT, LTCAUD, LTCETH, LTCGBP, LTCUSDT, MANAETH, MANAEUR, MANAUSD,')
        embed.set_thumbnail(url = bot.user.avatar_url)
        embed.set_footer(text = 'Requested by ' + ctx.author.name + '.', icon_url = ctx.author.avatar_url)
        await ctx.send(embed = embed)

        embed = discord.Embed(title = 'Pairs 2/2', color = 0x5741d9,
                        description = 'MANAXBT, NANOETH, NANOEUR, NANOUSD, NANOXBT, OCEANEUR, OCEANGBP, OCEANUSD, OCEANXBT, OMGETH, OMGEUR, OMGUSD, OMGXBT, OXTETH, OXTEUR, OXTUSD, OXTXBT, PAXGETH, PAXGEUR, PAXGUSD, PAXGXBT, QTUMETH, QTUMEUR, QTUMUSD, QTUMXBT, REPVETH, REPVEUR, REPVUSD, REPVXBT, SCETH, SCEUR, SCUSD, SCXBT, SNXAUD, SNXETH, SNXEUR, SNXGBP, SNXUSD, SNXXBT, STORJETH, STORJEUR, STORJUSD, STORJXBT, TBTCETH, TBTCEUR, TBTCUSD, TBTCXBT, TRXETH, TRXEUR, TRXUSD, TRXXBT, UNIETH, UNIEUR, UNIUSD, UNIXBT, USDCAUD, USDCEUR, USDCGBP, USDCHF, USDCUSD, USDCUSDT, USDTAUD, USDTCAD, USDTCHF, USDTEUR, USDTGBP, USDTJPY, USDTUSD, WAVESETH, WAVESEUR, WAVESUSD, WAVESXBT, XBTAUD, XBTCHF, XBTDAI, XBTUSDC, XBTUSDT, XDGEUR, XDGUSD, XETCETH, XETCXBT, XETCEUR, XETCUSD, XETHXBT, XETHCAD, XETHEUR, XETHGBP, XETHJPY, XETHUSD, XLTCXBT, XLTCEUR, XLTCJPY, XLTCUSD, XMLNETH, XMLNXBT, XMLNEUR, XMLNUSD, XREPETH, XREPXBT, XREPEUR, XREPUSD, XRPAUD, XRPETH, XRPGBP, XRPUSDT, XTZAUD, XTZETH, XTZEUR, XTZGBP, XTZUSD, XTZXBT, XXBTCAD, XXBTEUR, XXBTGBP, XXBTJPY, XXBTUSD, XXDGXBT, XXLMXBT, XXLMAUD, XXLMEUR, XXLMGBP, XXLMUSD, XXMRXBT, XXMREUR, XXMRUSD, XXRPXBT, XXRPCAD, XXRPEUR, XXRPJPY, XXRPUSD, XZECXBT, XZECEUR, XZECUSD, YFIAUD, YFIETH, YFIEUR, YFIGBP, YFIUSD, YFIXBT')
        embed.set_thumbnail(url = bot.user.avatar_url)
        embed.set_footer(text = 'Requested by ' + ctx.author.name + '.', icon_url = ctx.author.avatar_url)     
        await ctx.send(embed = embed)

    ### ECONOMY COMMANDS ###
    @bot.command()
    async def info(ctx, base, quote):
        crypto = base.upper() + quote.upper() # Generate name
        base = bases[base.upper()] # Convert human readable base to Kraken API base
        quote = quotes[quote.upper()] # Convert human readable quote to readable quote
        
        k = krakenex.API()

        # Load data for analysis
        data = k.query_public('OHLC', {'pair': pair[base + quote], 'interval': '60'})['result'][pair[base + quote]] 

        embed = discord.Embed(title = data[-1][4] + ' | ' + crypto, color = base_colors[base])
        embed.timestamp = datetime.utcnow().replace(tzinfo=pytz.utc)

        embed.set_footer(text = 'Requested by ' + ctx.author.name, icon_url = ctx.author.avatar_url) 
        embed.add_field(name = 'TA', value = ema_ta(data) + '\n' + macd(data))
        embed.set_thumbnail(url = base_urls[base])

        await ctx.send(embed = embed)

    bot.run(open("token.txt", "r").read())

if __name__ == "__main__":
    main()
