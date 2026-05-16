from flask import Flask, render_template_string, jsonify
import ccxt
import os

app = Flask(__name__)
exchange = ccxt.binance()

capital = 1000
btc = 0
profit_safe = 0
bot_on = False


def price():
    return exchange.fetch_ticker('BTC/USDT')['last']


HTML = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Crypto Bot</title>

<style>
body {background:#0f172a;color:white;text-align:center;font-family:Arial}
.card {background:#111827;margin:10px;padding:15px;border-radius:10px}
button {padding:12px;margin:5px;width:90%;border:none;border-radius:8px}
.green{background:green;color:white}
.red{background:red;color:white}
.orange{background:orange;color:black}
</style>

<script>
async function update(){
    let r = await fetch('/data')
    let d = await r.json()

    document.getElementById("p").innerText = "BTC: " + d.price
    document.getElementById("w").innerText = "Capital: " + d.capital + " | BTC: " + d.btc
    document.getElementById("pr").innerText = "Profit: " + d.profit
    document.getElementById("b").innerText = d.bot ? "🟢 BOT ON" : "🔴 BOT OFF"
}

async function buy(){ await fetch('/buy') }
async function sell(){ await fetch('/sell') }
async function bot(){ await fetch('/bot') }

setInterval(update,2000)
</script>

</head>

<body>

<h2>🤖 Crypto Bot</h2>

<div class="card" id="p"></div>
<div class="card" id="w"></div>
<div class="card" id="pr"></div>
<div class="card" id="b"></div>

<button class="green" onclick="buy()">BUY</button>
<button class="red" onclick="sell()">SELL</button>
<button class="orange" onclick="bot()">BOT ON/OFF</button>

</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(HTML)


@app.route("/data")
def data():
    global capital, btc, profit_safe

    p = price()

    total = capital + btc * p + profit_safe
    profit = total - 1000

    return jsonify({
        "price": round(p,2),
        "capital": round(capital,2),
        "btc": round(btc,6),
        "profit": round(profit,2),
        "bot": bot_on
    })


@app.route("/buy")
def buy():
    global capital, btc
    p = price()

    if capital > 0:
        btc = capital / p
        capital = 0

    return "ok"


@app.route("/sell")
def sell():
    global capital, btc, profit_safe
    p = price()

    if btc > 0:
        capital = btc * p
        btc = 0

        if capital > 1000:
            profit_safe += capital - 1000
            capital = 1000

    return "ok"


@app.route("/bot")
def bot():
    global bot_on
    bot_on = not bot_on
    return "ok"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)