from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <html>
    <head>
        <title>Crypto Bot IA</title>
        <style>
            body{
                background:#0f172a;
                color:white;
                font-family:Arial;
                text-align:center;
                padding-top:50px;
            }

            .card{
                background:#1e293b;
                width:350px;
                margin:auto;
                padding:30px;
                border-radius:20px;
                box-shadow:0 0 20px rgba(0,0,0,0.5);
            }

            h1{
                color:#facc15;
            }

            .price{
                font-size:40px;
                margin:20px;
            }

            button{
                background:#22c55e;
                color:white;
                border:none;
                padding:15px 30px;
                border-radius:10px;
                font-size:18px;
                cursor:pointer;
            }

            button:hover{
                background:#16a34a;
            }
        </style>
    </head>

    <body>

        <div class="card">
            <h1>🤖 Crypto Bot IA</h1>

            <p>Bot connecté avec Render</p>

            <div class="price">
                BTC : 103245 $
            </div>

            <button>BOT ACTIF</button>

            <p style="margin-top:20px;">
                Serveur en ligne ✅
            </p>
        </div>

    </body>
    </html>
    """

if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
