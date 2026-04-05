# =========================
# 🌐 WEB APP
# =========================
from flask import Flask, jsonify
from database import get_history

app = Flask(__name__)

@app.route("/")
def home():
    return "🔥 BOT BOOKMAKER PRO WEB ACTIF"

@app.route("/history")
def history():
    return jsonify(get_history())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)