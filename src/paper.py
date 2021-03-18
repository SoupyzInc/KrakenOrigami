import mysql.connector
from datetime import datetime

db = mysql.connector.connect(
  host="localhost",
  user="Okashita",
  password="L+E+7b__?3eK3&L#cCRsK9F",
  database="accounts"
)

def register(id):
    """
    Registers a user account into the account database.

    Args:
        id: The Discord user id of the user to be added.
    """
    
    print(datetime.utcnow().strftime("%y-%m-%d %H:%M:%S"))
    cursor = db.cursor()
    cursor.execute("INSERT INTO users (id) VALUES (%s)", (id,))
    db.commit()

def valid(id):
  """
  Checks if a user has made an account or not.

  Args:
      id: The Discord user id of the user to be querired.

  Returns:
    Boolean True if the user has an account and False if not.
  """

  cursor = db.cursor()
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

    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE id = " + str(id))
    for x in cursor:
        return x[1]

def buy(id, pair, price, amount):
    """
    Logs the purchase of a crypto.

    Args:
        id: The Discord user id of the user to executing the trade.
        pair: The pair to be traded (in the Kraken API format).
        price: The price of the crypto at purchase.
        amount: The amount of the crypto purchased (in dollars).
    """

    cursor = db.cursor()

    # Log trade
    cursor.execute("INSERT INTO open_trades (user_id, pair, price, amount) VALUES(%s, %s, %s, %s)", (id, pair, price, amount))

    # Make user pay for amount of crypto bought
    cursor.execute("""UPDATE users
                      SET balance = """ + str(get_balance(id) - amount) +
                   """WHERE id = """ + str(id))

    db.commit()


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
