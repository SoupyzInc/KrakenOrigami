<h1 align="center" >Kraken Origami</h1>
<p align="center">
  <img width="150" src="https://github.com/SoupyzInc/KrakenOrigami/blob/main/Wiki/K.png">
</p>

A WIP Discord bot written using [discord.py](https://github.com/Rapptz/discord.py) and [Krakenex](https://github.com/veox/python3-krakenex) to give techincal analysis on crypto, in Discord.

![](https://github.com/SoupyzInc/KrakenOrigami/blob/main/Wiki/LTC%20Example.png)

### Installation 
If you wish to use this bot, you can download and run the code your self.
1. Download the code from the [`src` folder](https://github.com/SoupyzInc/KrakenOrigami/tree/main/src) of this repository.
2. Create a Discord bot and get your token.
3. Replace the token in `token.txt` with your token. _Do not ever share your token with anyone._
4. Install dependencies. I used [python 3.9.2](https://www.python.org/downloads/), [discord.py](https://github.com/Rapptz/discord.py), and [Krakenex](https://github.com/veox/python3-krakenex).
5. Run the `bot.py` file, your bot should be online and ready to run now.

### Current Features
This is what the bot can do right now.
- Give the current price of any crypto on [Kraken](https://api.kraken.com/0/public/AssetPairs) (not including forex).
- Give technical analysis based on:
  - EMA clouds. Utilizing 10, 20, 30, and 40 EMA clouds, the bot can suggest entry, hold, and exit points.

### Up Next
This is what I plan to do next with this bot.
- Implement MACD.
- Implement RSI.
- Create a paper trading system.
  - Have the bot trade on its own using the paper trading system. The bot will use EMA, MACD, and RSI to create entries and find exits.
  - Allow people to paper trade as well.
- Implement robust TA involving multiple time periods (1hr, 30 min, 15 min, 3 min).
