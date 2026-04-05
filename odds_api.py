# =========================
# 📡 BOOKMAKER API CONNECTOR
# =========================
import os
import requests

API_KEY = os.getenv("ODDS_API_KEY")

def fetch_odds(home, away):
    if not API_KEY:
        return None

    try:
        url = "https://api.the-odds-api.com/v4/sports/soccer/odds/"
        params = {
            "apiKey": API_KEY,
            "regions": "eu",
            "markets": "h2h,totals,btts"
        }

        res = requests.get(url, params=params, timeout=10)
        data = res.json()

        for match in data:
            teams = match.get("teams", [])
            if home in teams and away in teams:
                return match

    except Exception as e:
        print("ODDS API ERROR:", e)

    return None
