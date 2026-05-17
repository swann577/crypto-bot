from flask import Flask, render_template_string
import random
import sqlite3
import requests
import json
import os
import time

app = Flask(__name__)

# =========================
# DATABASE
# =========================

DB_FILE = "bot.db"
SAVE_FILE = "bot_data.json"


def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS bot (
            id INTEGER PRIMARY KEY,
            capital REAL,
            profit_wallet REAL,
            trades INTEGER
        )
    ''')

    c.execute('SELECT * FROM bot WHERE id = 1')
    existing = c.fetchone()

    if not existing:
        c.execute(
            'INSERT INTO bot (id, capital, profit_wallet, trades) VALUES (1, 100, 0, 0)'
        )

    conn.commit()
    conn.close()


init_db()


# =========================
# SQLITE FUNCTIONS
# =========================


def get_bot_data():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    c.execute('SELECT capital, profit_wallet, trades FROM bot WHERE id = 1')
    data = c.fetchone()

    conn.close()

    return {
        "capital": data[0],
        "profit_wallet": data[1],
        "trades_count": data[2]
    }



def save_bot_data(capital, profit_wallet, trades_count):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    c.execute('''
        UPDATE bot
        SET capital=?, profit_wallet=?, trades=?
        WHERE id=1
    ''', (capital, profit_wallet, trades_count))

    conn.commit()
    conn.close()


# =========================
# BOT
# =========================

bot = {
    "active": True,
    "btc_price": 0,
    "last_trade_time": 0,
    "trades": []
}


# =========================
# SAVE JSON
# =========================


def save_data():
    with open(SAVE_FILE, "w") as f:
        json.dump(bot, f)



def load_data():
    global bot

    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            loaded = json.load(f)

            bot["trades"] = loaded.get("trades", [])
            bot["btc_price"] = loaded.get("btc_price", 0)
            bot["last_trade_time"] = loaded.get("last_trade_time", 0)


load_data()


# =========================
# BTC PRICE
# =========================


def get_btc_price():
    try:
        url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
        data = requests.get(url).json()
        return round(float(data["price"]), 2)
    except:
        return random.randint(60000, 70000)


# =========================
# TRADING LOGIC
# =========================


def trade_logic():
    now = time.time()

    # 1 trade max toutes les 30 sec
    if now - bot["last_trade_time"] < 30:
        return

    bot["last_trade_time"] = now

    data = get_bot_data()

    capital = data["capital"]
    profit_wallet = data["profit_wallet"]

    bot["btc_price"] = get_btc_price()

    rsi = random.randint(20, 80)

    action = "HOLD"
    profit = 0

    if rsi < 35:
        action = "BUY"
        profit = round(random.uniform(0.5, 2.5), 2)

    elif rsi > 65:
        action = "SELL"
        profit = round(random.uniform(-1.5, 1.5), 2)

    if action != "HOLD":

        if profit > 0:
            profit_wallet += profit
        else:
            capital += profit

        save_bot_data(
            capital,
            profit_wallet,
            len(bot["trades"])
        )

        trade = {
            "action": action,
            "profit": profit,
            "btc_price": bot["btc_price"],
            "rsi": rsi
        }

        bot["trades"].insert(0, trade)

        # max 50 trades
        bot["trades"] = bot["trades"][:50]

        save_data()


# =========================
# PAGE WEB
# =========================


@app.route("/")
def home():

    if bot["active"]:
        trade_logic()

    data = get_bot_data()

    capital = data["capital"]
    profit_wallet = data["profit_wallet"]

    html = """
    <html>
    <head>
        <title>Crypto Bot Pro</title>

        <meta name="viewport" content="width=device-width, initial-scale=1">

        <style>

            body{
                background:#0f172a;
                color:white;
                font-family:Arial;
                padding:20px;
            }

            .card{
                background:#1e293b;
                padding:20px;
                border-radius:15px;
                margin-bottom:20px;
            }

            h1{
                color:#38bdf8;
            }

            .profit{
                color:#22c55e;
                font-size:22px;
            }

            .loss{
                color:#ef4444;
            }

        </style>
    </head>

    <body>

        <h1>🤖 Crypto Bot Pro</h1>

        <div class="card">
            <h2>📊 Capital</h2>
            <p>{{capital}} €</p>
        </div>

        <div class="card">
            <h2>💰 Profit Wallet</h2>
            <p class="profit">{{profit}} €</p>
        </div>

        <div class="card">
            <h2>₿ BTC Price</h2>
            <p>{{btc}} $</p>
        </div>

        <div class="card">
            <h2>📈 Trades</h2>

            {% for trade in trades %}

                <p>
                    {{trade.action}}
                    |
                    RSI {{trade.rsi}}
                    |
                    BTC {{trade.btc_price}} $
                    |
                    <span class="{% if trade.profit >=0 %}profit{% else %}loss{% endif %}">
                        {{trade.profit}} €
                    </span>
                </p>

            {% endfor %}

        </div>

    </body>
    </html>
    """

    return render_template_string(
        html,
        capital=round(capital, 2),
        profit=round(profit_wallet, 2),
        btc=bot["btc_price"],
        trades=bot["trades"]
    )


# =========================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
