import mysql.connector
import pytz
import krakenex
import discord
from ta import convert, get_ohlc
from pairs import base_urls
from datetime import datetime

db = mysql.connector.connect(
)

def register(id):
    """
    Registers a user account into the account database.

    Args:
        id: The Discord user id of the user to be added.
    """

    print(datetime.utcnow().strftime("%y-%m-%d %H:%M:%S"))
    cursor = db.cursor(buffered=True)
    cursor.execute("INSERT INTO users (id) VALUES (%s)", (id,))
    db.commit()

def valid(id):
  """
  Checks if a user has made an account or not.

  Args:
      id: The Discord user id of the user to be queried.

  Returns:
    Boolean True if the user has an account and False if not.
  """

  cursor = db.cursor(buffered=True)
  cursor.execute("SELECT id FROM users")

  for x in cursor:
      for user_ids in x:
          if user_ids == id:
              return True

  return False

def get_balance(id):
    """
    Gets a user's balance from the account SQL database.

    Args:
        id: The Discord user id of the user to be queried.

    Returns:
        A string of the user's balance.
    """

    cursor = db.cursor(buffered=True)
    cursor.execute("SELECT * FROM users WHERE id = " + str(id))
    for x in cursor:
        return x[1]

def get_positions(id):
    """
    Gets a user's open positions.

    Args:
        id:  The Discord user id of the user to be queried.

    Returns:
        A list of trades, which are tuples in the format: (id, user_id, pair, time of trade, price of crypto at purchase, amount purchased).
    """
    cursor = db.cursor(buffered=True)
    cursor.execute("SELECT * FROM open_trades WHERE user_id = " + str(id))

    out = []
    for x in cursor:
        out.append(x)

    return out

def buy(id, pair, price, amount):
    """
    Logs the purchase of a crypto.

    Args:
        id: The Discord user id of the user to executing the trade.
        pair: The pair to be traded (in the Kraken API format).
        price: The price of the crypto at purchase.
        amount: The amount of the crypto purchased (in dollars).
    """

    cursor = db.cursor(buffered=True)

    # Log trade
    cursor.execute("INSERT INTO open_trades (user_id, pair, price, amount) VALUES(%s, %s, %s, %s)", (id, pair, price, amount))

    # Make user pay for amount of crypto bought
    cursor.execute("""UPDATE users
                      SET balance = """ + str(get_balance(id) - amount) +
                   """WHERE id = """ + str(id))

    db.commit()

def valid_close(user_id, trade_id):
    cursor = db.cursor(buffered=True)
    cursor.execute("""SELECT * FROM open_trades
                               GROUP BY """)
    for x in cursor:
        for y in x:
            print(y)

def close(user_id, close, ctx): #, 
    cursor = db.cursor(buffered=True)

    # Get open positions that the user opened
    if (len(get_positions(user_id)) > 0):
        cursor.execute("SELECT GROUP_CONCAT(id), COUNT(user_id) c FROM open_trades GROUP BY user_id HAVING c > 1")

        single = True
        conversion = [-1]
        for x in cursor:
            data = x[0]
            single = False

        if single:
            cursor.execute("SELECT id FROM open_trades WHERE user_id = " + str(user_id))
            for x in cursor:
                data = x
            for x in data:
                conversion.append(x)
        else:
            for x in data.split(','):
                conversion.append(x)

        if int(close) <= len(conversion) and int(close) > 0:
            # Calculate values
            cursor.execute("SELECT * FROM open_trades WHERE id = " + str(conversion[int(close)]))
            for x in cursor:
                position = x
                # (6, 344671380412956673, 'XLTCZUSD', datetime.datetime(2021, 3, 18, 0, 26, 36), 205.46, 100.0)
                # (id, user_id, pair, time of trade, price of crypto at purchase, amount purchased)
                # (0,  1,       2,    3,             4,                           5)

            price_close = float(get_ohlc(position[2])[4])
            return_percent = ((price_close - position[4])/ position[4]) * 100
            shares = position[5] / position[4]
            return_decimal = (shares * price_close) - (shares * position[4])

            # Log trade as now closed
            cursor.execute("""INSERT INTO closed_trades (user_id, pair, time_open, price_open, price_close, amount, return_percent, return_decimal) 
                            VALUES(%s, %s, %s, %s, %s, %s, %s, %s)""", 
                            (user_id, position[2], position[3], position[4], price_close, position[5], return_percent, return_decimal))
            db.commit()

            # Remove open position
            cursor.execute("DELETE FROM open_trades WHERE id = " + str(conversion[int(close)]))
            db.commit()

            # Add profits (or lack of) to balance
            balance = get_balance(user_id) + return_decimal

            cursor.execute("""UPDATE users
                        SET balance = """ + str(balance) +
                    """WHERE id = """ + str(user_id))
            db.commit()   

            if return_decimal > 0:
                color = 0x43B581
            elif return_decimal < 0:
                color = 0xF04747
            else:
                color = 0x202225

            embed = discord.Embed(title = ctx.author.name + " closed " + str(position[2]), color = color)

            if (return_percent > 0):
                percent = "+" + str(round(return_percent, 2)) + "%"
                numerical = "+" + "${:,.2f}".format(return_decimal)
            elif (return_percent < 0):
                percent = str(round(return_percent, 2)) + "%"
                return_decimal *= -1
                numerical = "-" + "${:,.2f}".format(return_decimal)
            else:
                percent = str(round(return_percent, 2)) + "%"
                numerical = "${:,.2f}".format(return_decimal)

            out = "\n`" + percent + "` " + numerical + "\n> ${:,.2f}".format(position[5]) + " @ " + "${:,.2f}".format(position[4]) + " on " + str(position[3])

            embed.add_field(name = str(position[2]), value = str(position[4]) + " 🠒 " + str(price_close) + 
                        "\n" + out)
            # embed.timestamp = datetime.utcnow().replace(tzinfo=pytz.utc)
            embed.set_footer(text = 'Closed on ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            # embed.set_thumbnail(url = base_urls[base])

            return embed
            # return 'Position `' + position[2] + ' | ' + str(position[5]) + ' @ ' + str(position[4]) + "` successfully closed."
        else:
            return 'You only have ' + str(len(conversion)) + ' positions opened.'
    else:
        return 'You do not have any positions opened. Use `.buy help` to learn how to buy crypto.'
### Creation of the account database tables:
# cursor = db.cursor()

# cursor.execute("CREATE TABLE users (id BIGINT PRIMARY KEY, balance float DEFAULT 1000, open DATETIME DEFAULT CURRENT_TIMESTAMP)")

# cursor.execute("""CREATE TABLE open_trades (id BIGINT PRIMARY KEY AUTO_INCREMENT,
#                                             user_id BIGINT,
#                                             INDEX user_ind (user_id),
#                                             FOREIGN KEY (user_id) REFERENCES users(id), 
#                                             pair VARCHAR(10), 
#                                             time DATETIME DEFAULT CURRENT_TIMESTAMP,
#                                             price float, 
#                                             amount float)""")

# cursor.execute("""CREATE TABLE closed_trades (id BIGINT PRIMARY KEY AUTO_INCREMENT,
#                                               user_id BIGINT,
#                                               INDEX user_ind (user_id),
#                                               FOREIGN KEY (user_id) REFERENCES users(id),
#                                               pair VARCHAR(10), 
#                                               time_open DATETIME, 
#                                               time_close DATETIME DEFAULT CURRENT_TIMESTAMP,
#                                               price_open float, 
#                                               price_close float,
#                                               amount float, 
#                                               return_percent float,
#                                               return_decimal float)""")

# db.commit()
###
