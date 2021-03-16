# Kraken Origami
A WIP Discord bot written using [discord.py](https://github.com/Rapptz/discord.py) and [Krakenex](https://github.com/veox/python3-krakenex) to give data on crypto, in Discord.

Note: as of current, the SMA calculations are incorrect. They appear to be higher than the SMA values provided by [Kraken](trade.kraken.com).

![](https://github.com/SoupyzInc/KrakenOrigami/blob/main/Wiki/LTC%20Example.png)

### Installation 
If you wish to use this bot, you can download and run the code your self.
1. Download the code from the [`src` folder](https://github.com/SoupyzInc/KrakenOrigami/tree/main/src) of this repository.
2. Make an account with Kraken and create an API key. The API key will disppear once you save the API key and close the window, so make sure to save it now. _Note: It is safer to make the key only able to query information and not execute trades._
3. Replace the secret and key in `kraken.key` with your secret and key. _Do not ever share your secret or key with anyone._
4. Create a Discord bot and get your token.
5. Replace the token in `token.txt` with your token. _Do not ever share your token with anyone._
6. Install dependencies. I used [python 3.9.2](https://www.python.org/downloads/), [discord.py](https://github.com/Rapptz/discord.py), and [Krakenex](https://github.com/veox/python3-krakenex).
8. Run the `bot.py` file, your bot should be online and ready to run now.
