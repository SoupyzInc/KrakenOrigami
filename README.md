<p align="center">
  <img width="150" src="https://github.com/SoupyzInc/KrakenOrigami/blob/main/Wiki/K.png" alt="Kraken Origami Logo">
</p>
<h1 align="center" >Kraken Origami</h1>

A Discord bot written using [discord.py](https://github.com/Rapptz/discord.py), [krakenex](https://github.com/veox/python3-krakenex), and [MySQL](https://dev.mysql.com/downloads/installer/) to give paper trading for crypto.

![A showcase of some of Kraken Origami's commands.](https://github.com/SoupyzInc/KrakenOrigami/blob/main/Wiki/Kraken_Showcase.png)

### Installation 
If you wish to use this bot, you can download and run the code your self.
1. Clone this repostiory.
2. Create a Discord bot and get your token.
3. Replace the token in [`token.txt`](https://github.com/SoupyzInc/KrakenOrigami/blob/main/src/token.txt) with your token. _Do not ever share your token with anyone._
5. Install dependencies. I used [python 3.9.2](https://www.python.org/downloads/), [discord.py 1.6.0](https://github.com/Rapptz/discord.py), [pytz 2020.5](https://pypi.org/project/pytz/), [krakenex 2.1.0](https://github.com/veox/python3-krakenex), [MySQL](https://dev.mysql.com/downloads/installer/), and [MySQL Connector Python 8.0.23](https://dev.mysql.com/downloads/connector/python/).
6. Replace the information in [`mysql_account.txt`](https://github.com/SoupyzInc/KrakenOrigami/blob/main/src/sql_account.txt) with your information. _Do not ever share your credentials with anyone._
7. Create a `discord.log` file in the `src` folder to allow `bot.py` to log events and warnings.
8. Run the `bot.py` file, your bot should be online and ready to run now.

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
