from tkinter import *
from tkinter import messagebox, Menu
import requests
import json
import sqlite3

pycrypto = Tk()
pycrypto.title("My Crypto Portfolio")

connection = sqlite3.connect('coin.db')
cursorObject = connection.cursor()
cursorObject.execute("CREATE TABLE IF NOT EXISTS coin(id INTEGER PRIMARY KEY, symbol TEXT, amount INTEGER, price REAL)")
connection.commit()

# example of insert query 
# cursorObject.execute("INSERT INTO coin VALUES(1, 'BTC', 2, 3250)")
# connection.commit()

# pycrypto.iconbitmap('icons8-cryptocurrency-32.png')

def myportfolio():
    ## create a variable to store API data into 
    api_requests = requests.get("https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?start=1&limit=300&convert=USD&CMC_PRO_API_KEY=")

    ## create a variable to parses the data into a JSON variable 
    api = json.loads(api_requests.content)
    
    # A Fetch using the cursor object 
    cursorObject.execute("SELECT * FROM coin")
    coins = cursorObject.fetchall()

    def font_color(amount):
        if amount >= 0: 
            return "green"
        else: 
            return "red"

    def insert_coin():
        cursorObject.execute("INSERT INTO coin(symbol, price, amount) VALUES(?, ?, ?)", (symbol_txt.get(), price_txt.get(), amount_txt.get()))
        connection.commit()

    def update_coin():
        cursorObject.execute("UPDATE coin SET symbol=?, price=?, amount=? WHERE id=?", (symbol_update.get(), price_update.get(), amount_update.get(), portid_update.get()))
        connection.commit()

    ## in parameters display specific data you want to display
    # print(api["data"][0]["symbol"])
    # print(api["data"][0]["quote"]["USD"]["price"])

    # creating a dictionary for ea. coin I have invested in hypothetically 
    coins = [
        {
        "symbol": "BTC",
        "amount_owned": 1,
        "price_per_coin": 30000,
        },
        {
        "symbol": "ETH",
        "amount_owned": 1,
        "price_per_coin": 2100,
        },
        {
        "symbol": "USDT",
        "amount_owned": 1,
        "price_per_coin": .98,
        },
        {
        "symbol": "USDC",
        "amount_owned": 1,
        "price_per_coin": .99,
        },
        {
        "symbol": "BNB",
        "amount_owned": 1,
        "price_per_coin": 300,
        },
        ]

    total_pl = 0
    coin_row = 1
    total_current_value = 0
    total_amount_paid = 0

    # i is printing the index of the top 5 bitcoins 
    for i in range(0, 300):
        for coin in coins:
            if api["data"][i]["symbol"] == coin[1]:
                total_paid = coin[2] * coin[3]
                current_value = coin[2] * api["data"][i]["quote"]["USD"]["price"]
                pl_percoin = api["data"][i]["quote"]["USD"]["price"] - coin[3]
                total_pl_coin = pl_percoin * coin[2]

                total_pl += total_pl_coin
                total_current_value += current_value
                total_amount_paid += total_paid

                # print((api["data"][i]["name"]) + " - " + (api["data"][i]["symbol"]))
                # print("{0:.2f}".format(api["data"][i]["quote"]["USD"]["price"]))
                # print("Number Of Coin: ", coin[2])
                # print("Total Amount Paid: ", "{0:.2f}".format(total_paid))
                # print("Current Value: ", "{0:.2f}".format(current_value))
                # print("Profit/Loss Per Coin: ", "{0:.2f}".format(pl_percoin))
                # print("Total P/L With Coin: ", "{0:.2f}".format(total_pl_coin))
                # print("-----------------")

                portfolio_id = Label(pycrypto, text=coin[0], fg="black", bg="white", font="lato 12", borderwidth=2, relief="groove")
                portfolio_id.grid(row=coin_row, column=0, sticky=N+S+E+W)

                name = Label(pycrypto, text=api["data"][i]["symbol"], bg="white", fg="black", borderwidth=2, relief="groove", padx="2", pady="2")
                name.grid(row=coin_row,column=1, sticky=N+S+E+W)

                price = Label(pycrypto, text="{0:.2f}".format(api["data"][i]["quote"]["USD"]["price"]), bg="white", fg="black", borderwidth=2, relief="groove", padx="2", pady="2")
                price.grid(row=coin_row,column=2, sticky=N+S+E+W)

                no_coins = Label(pycrypto, text=coin[2], bg="white", fg="black", borderwidth=2, relief="groove", padx="2", pady="2")
                no_coins.grid(row=coin_row,column=3, sticky=N+S+E+W)

                amount_paid = Label(pycrypto, text="{0:.2f}".format(total_paid), bg="white", fg="black", borderwidth=2, relief="groove", padx="2", pady="2")
                amount_paid.grid(row=coin_row,column=4, sticky=N+S+E+W)

                current_value = Label(pycrypto, text="{0:.2f}".format(current_value), bg="white", fg="black", borderwidth=2, relief="groove", padx="2", pady="2")
                current_value.grid(row=coin_row,column=5, sticky=N+S+E+W)

                pl_coin = Label(pycrypto, text="{0:.2f}".format(pl_percoin), bg="white", fg=font_color(float("{0:.2f}".format(pl_percoin))), borderwidth=2, relief="groove", padx="2", pady="2")
                pl_coin.grid(row=coin_row,column=6, sticky=N+S+E+W)

                total_pl = Label(pycrypto, text="{0:.2f}".format(total_pl_coin), bg="white", fg=font_color(float("{0:.2f}".format(total_pl_coin))), borderwidth=2, relief="groove", padx="2", pady="2")
                total_pl.grid(row=coin_row,column=7, sticky=N+S+E+W)

                coin_row += 1 

    # Insert Data 
    symbol_text = Entry(pycrypto, borderwidth=2, relief="groove")
    symbol_text.grid(row=coin_row+1, column=1)

    price_txt = Entry(pycrypto, borderwidth=2, relief="groove")
    price_txt.grid(row=coin_row+1, column=2)

    amount_txt = Entry(pycrypto, borderwidth=2, relief="groove")
    amount_txt.grid(row=coin_row+1, column=3)

    add_coin = Button(pycrypto, text="Add Coin", bg="dark slate grey", fg="white", command=insert_coin ,font="Lato 12", borderwidth=2, relief="groove", padx="2", pady="2")
    add_coin.grid(row=coin_row + 1, column=4, sticky=N+S+E+W)

    # Update Coin 
    portid_update = Entry(pycrypto, borderwidth=2, relief="groove")
    portid_update.grid(row=coin_row+2, column=0)

    symbol_update = Entry(pycrypto, borderwidth=2, relief="groove")
    symbol_update.grid(row=coin_row+2, column=1)

    price_update = Entry(pycrypto, borderwidth=2, relief="groove")
    price_update.grid(row=coin_row+2, column=2)

    amount_update = Entry(pycrypto, borderwidth=2, relief="groove")
    amount_update.grid(row=coin_row+2, column=3)

    update_coin_txt = Button(pycrypto, text="Update Coin", bg="#142E54", fg="white", command=update_coin,font="Lato 12", borderwidth=2, relief="groove", padx="2", pady="2")
    update_coin_txt.grid(row=coin_row + 2, column=4, sticky=N+S+E+W)

    total_amount_paid = Label(pycrypto, text="{0:.2f}".format(total_current_value), bg="white", fg="black", borderwidth=2, relief="groove", padx="2", pady="2")
    total_amount_paid.grid(row=coin_row,column=4, sticky=N+S+E+W)

    totalcv = Label(pycrypto, text="{0:.2f}".format(total_current_value), bg="white", fg="black", borderwidth=2, relief="groove", padx="2", pady="2")
    totalcv.grid(row=coin_row,column=4, sticky=N+S+E+W)

    total_pl = Label(pycrypto, text="{0:.2f}".format(total_pl), bg="white", fg=font_color(float("{0:.2f}".format(total_pl))), borderwidth=2, relief="groove", padx="2", pady="2")
    total_pl.grid(row=coin_row,column=6, sticky=N+S+E+W)

    api = ""

    refresh = Button(pycrypto, text="Refresh", bg="dark slate gray", fg="white", borderwidth=2, command = myportfolio,  relief="groove", padx="2", pady="2", font="lato 12")
    refresh.grid(row=coin_row + 1,column=6, sticky=N+S+E+W)

def application_header():
    portfolio_id = Label(pycrypto, text="Portfolio ID", bg="dark slate gray", fg="white", font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
    portfolio_id.grid(row=0, column=0, sticky=N+S+E+W)

    name = Label(pycrypto, text="Coin Name", bg="dark slate gray", fg="white", font="lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
    name.grid(row=0,column=0, sticky=N+S+E+W)

    price = Label(pycrypto, text="Price", bg="dark slate gray", fg="white", font="lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
    price.grid(row=0,column=1, sticky=N+S+E+W)

    no_coins = Label(pycrypto, text="Coin Owned", bg="dark slate gray", fg="white", font="lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
    no_coins.grid(row=0,column=2, sticky=N+S+E+W)

    amount_paid = Label(pycrypto, text="Total Amount Paid", bg="dark slate gray", fg="white", font="lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
    amount_paid.grid(row=0,column=3, sticky=N+S+E+W)

    current_value = Label(pycrypto, text="Current Value", bg="dark slate gray", fg="white", font="lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
    current_value.grid(row=0,column=4, sticky=N+S+E+W)

    pl_coin = Label(pycrypto, text="P/L Per Coin", bg="dark slate gray", fg="white", font="lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
    pl_coin.grid(row=0,column=5, sticky=N+S+E+W)

    total_pl = Label(pycrypto, text="Total P/L With Coin", bg="dark slate gray", fg="white", font="lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
    total_pl.grid(row=0,column=6, sticky=N+S+E+W)

myportfolio()
application_header()

pycrypto.mainloop()
print("program completed")

cursorObject.close()
connection.close()