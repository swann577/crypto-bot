from flask import Flask, jsonify
import random
import time

app = Flask(__name__)

# État global du bot (simulation)
bot = {
    "active": False,
    "capital": 1000,
    "profit": 0,
    "price": 65000
}

# Simule le marché
def update_price():
    change = random.uniform(-500, 500)
    bot["price"] = max(1000, bot["price"] + change)

# Simule trading
def trade_logic():
    if not bot["active"]:
        return

    update_price()

    rsi = random.randint(10, 90)

    # stratégie simple
    if rsi < 30:
        gain = random.uniform(1, 10)
        bot["profit"] += gain
    elif rsi > 70:
        loss = random.uniform(1, 8)
        bot["profit"] -= loss

@app.route("/")
def home():
    trade_logic()

    status = "🟢 ACTIF" if bot["active"] else "🔴 STOP"

    return f"""
    <html>
    <head>
        <title>Crypto Bot PRO</title>
        <style>
            body {{
                margin:0;
                font-family:Arial;
                background:#0b1220;
                color:white;
            }}

            .container {{
                max-width:500px;
                margin:50px auto;
                padding:20px;
                background:#111a2e;
                border-radius:20px;
                text-align:center;
                box-shadow:0 0 20px rgba(0,0,0,0.5);
            }}

            h1 {{
                color:#facc15;
            }}

            .box {{
                background:#1f2a44;
                padding:15px;
                margin:10px 0;
                border-radius:12px;
            }}

            .price {{
                font-size:28px;
                color:#22c55e;
            }}

            button {{
                padding:15px 25px;
                border:none;
                border-radius:10px;
                font-size:16px;
                cursor:pointer;
                background:#3b82f6;
                color:white;
                margin-top:10px;
            }}

            button:hover {{
                background:#2563eb;
            }}
        </style>
    </head>

    <body>
        <div class="container">
            <h1>🤖 Crypto Bot IA PRO</h1>

            <div class="box">
                Statut : {status}
            </div>

            <div class="box price">
                BTC : {round(bot["price"], 2)} $
            </div>

            <div class="box">
                💰 Profit : {round(bot["profit"], 2)} $
            </div>

            <a href="/toggle">
                <button>ON / OFF BOT</button>
            </a>

            <p style="margin-top:20px;font-size:12px;color:gray;">
                Simulation trading - Render Cloud
            </p>
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
