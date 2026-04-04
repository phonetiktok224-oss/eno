# api_server.py

from flask import Flask, jsonify
from data_sources import get_all_matches

app = Flask(__name__)

@app.route("/matches")
def matches():
    return jsonify(get_all_matches())


def run_api():
    app.run(port=5000)