from flask import Flask, jsonify
import random

app = Flask(__name__)

bot = {
    "active": False,
    "capital_base": 100.0,   # capital initial
    "capital_used": 100.0,   # toujours réinvesti
    "profit_wallet": 0.0,    # profits stockés
    "price": 60000,
    "trades": []
}

def market_move():
    bot["price"] += random.uniform(-250, 250)

def signal():
    rsi = random.randint(10, 90)
    return rsi

def trade_logic():
    if not bot["active"]:
        return

    market_move()
    rsi = signal()

    action = "HOLD"
    profit = 0

    # stratégie simple intelligente simulée
    if rsi < 30:
        profit = random.uniform(0.5, 3.0)
        bot["capital_used"] = bot["capital_base"]  # réinvesti
        bot["profit_wallet"] += profit
        action = "BUY"

    elif rsi > 70:
        profit = -random.uniform(0.5, 2.0)
        bot["profit_wallet"] += profit
        action = "SELL"

    bot["trades"].append({
        "price": round(bot["price"], 2),
        "rsi": rsi,
        "action": action,
        "profit_wallet": round(bot["profit_wallet"], 2)
    })

@app.route("/")
def home():
    trade_logic()

    status = "🟢 ACTIF" if bot["active"] else "🔴 STOP"

    return f"""
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Crypto Bot iPhone PRO</title>
        <style>
            body {{
                margin:0;
                font-family:-apple-system;
                background:#0b1220;
                color:white;
                text-align:center;
            }}

            .card {{
                background:#111a2e;
                margin:20px;
                padding:20px;
                border-radius:20px;
            }}

            .title {{
                font-size:22px;
                font-weight:bold;
                color:#facc15;
            }}

            .price {{
                font-size:28px;
                color:#22c55e;
            }}

            .profit {{
                font-size:22px;
                color:#38bdf8;
            }}

            button {{
                padding:15px;
                width:90%;
                border:none;
                border-radius:12px;
                background:#3b82f6;
                color:white;
                font-size:18px;
            }}
        </style>
    </head>

    <body>

        <div class="card">
            <div class="title">🤖 Crypto Bot iPhone PRO</div>
            <p>Statut : {status}</p>
        </div>

        <div class="card price">
            BTC : {round(bot["price"],2)} $
        </div>

        <div class="card profit">
            💰 Profit wallet : {round(bot["profit_wallet"],2)} €
        </div>

        <div class="card">
            📊 Capital réinvesti : {bot["capital_base"]} €
        </div>

        <a href="/toggle">
            <button>ON / OFF BOT</button>
        </a>

        <div class="card">
            📈 Trades : {len(bot["trades"])}
        </div>

    </body>
    </html>
    """

@app.route("/toggle")
def toggle():
    bot["active"] = not bot["active"]
    return "<script>window.location.href='/'</script>"

@app.route("/data")
def data():
    return jsonify(bot)

if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
