<p align="center">
  <img width="150" src="https://github.com/SoupyzInc/KrakenOrigami/blob/main/Wiki/K.png" alt="Kraken Origami Logo">
</p>
<h1 align="center" >Kraken Origami</h1>

A WIP Discord bot written using [discord.py](https://github.com/Rapptz/discord.py), [Krakenex](https://github.com/veox/python3-krakenex), and [MySQL](https://dev.mysql.com/downloads/installer/) to give technical analysis and paper trading for crypto.

![A showcase of some of Kraken Origami's commands.](https://github.com/SoupyzInc/KrakenOrigami/blob/main/Wiki/Kraken_Showcase.png)

### Installation 
If you wish to use this bot, you can download and run the code your self.
1. Download the code from the [`src` folder](https://github.com/SoupyzInc/KrakenOrigami/tree/main/src) of this repository.
2. Create a Discord bot and get your token.
3. Replace the token in [`token.txt`](https://github.com/SoupyzInc/KrakenOrigami/blob/main/src/token.txt) with your token. _Do not ever share your token with anyone._
5. Install dependencies. I used [python 3.9.2](https://www.python.org/downloads/), [discord.py 1.6.0](https://github.com/Rapptz/discord.py), [pytz 2020.5](https://pypi.org/project/pytz/), [Krakenex 2.1.0](https://github.com/veox/python3-krakenex), [MySQL](https://dev.mysql.com/downloads/installer/), and [MySQL Connector Python 8.0.23](https://dev.mysql.com/downloads/connector/python/).
6. Replace the information in [`mysql_account.txt`](https://github.com/SoupyzInc/KrakenOrigami/blob/main/src/sql_account.txt) with your information. _Do not ever share your credentials with anyone._
7. Create a `discord.log` file in the `src` folder to allow `bot.py` to log events and warnings.
8. Run the `bot.py` file, your bot should be online and ready to run now.

### Features
In no particular order
- [x] Give the current price of any crypto on [Kraken](https://api.kraken.com/0/public/AssetPairs) (excluding forex).
- [ ] Give technical analysis based on:
  - [x] EMA clouds. Utilizing 10, 20, 30, and 40 EMA clouds, the bot can suggest entry, hold, and exit points.
  - [ ] MACD. Utilize the strength and duration of MACD trends to find trend reversals.
  - [ ] RSI. Utilize breakouts from the overbought and oversold positions to find trend reversals.
  - [ ] Apply TA from across multiple time periods to have proper entries.
- [ ] Create a paper trading system.
  - [ ] Have the bot trade on its own using this paper trading system. The bot will use the mentioned TA to trade.
  - [x] Allow users to trade as well, similar to leagues on Invstr (buys only, no shorts; no hedgies).
  - [x] Users should be able to execute trades and close positions, check positions, and see profits on their entire portfolio and individual positions.
- [ ] Host the bot on a server or Raspberry Pi.
  - [ ] Allows the bot and trading algorithm to run 24/7.
  - [ ] Be able to notify users for good entries on their watchlist, good exits on their current positions, and give price alerts.
- [ ] Host the MySQL database off of a Raspberry Pi and be able to establish remote connection from my laptop
- [ ] Establish "offline" functionality when a connection cannot be established with the database.
- [ ] Fine tune the trading algoritm to a point where I can confidently have it trade with real money.

### Commands
All of Kraken Origami's commands. The folling convetions are used: `<Required Parameter> (Optional Parameter)`

`.help (Command)`

Shows how a list of all commands or details how to use a specific command.

`.pairs`

Returns all possible pairs in two messages.

`.info <Base> <Quote>`

Gives technical analysis on the requeted pair (Base/Quote).

`.register`

Registers an account to begin paper trading.

`.account (@User)`

Returns your account or the pinged user's account.

`.buy <Base> <Quote> <Amount>`

Buys <Amount> in dollars of the specified pair.
  
`.close <Position #>`

Closes your position. Position numbers are listed when you use `.account`.
