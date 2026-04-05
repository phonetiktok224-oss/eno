# =========================
# 📡 ODDS API MULTI-KEY
# =========================
import os
import requests

API_KEYS = os.getenv("ODDS_API_KEY", "").split(",")

def fetch_odds(home, away):
    if not API_KEYS or API_KEYS == [""]:
        return None

    for key in API_KEYS:
        try:
            url = "https://api.the-odds-api.com/v4/sports/soccer/odds/"
            params = {
                "apiKey": key.strip(),
                "regions": "eu",
                "markets": "h2h,totals,btts"
            }

            res = requests.get(url, params=params, timeout=10)

            if res.status_code != 200:
                continue

            data = res.json()

            for match in data:
                teams = match.get("teams", [])
                if home in teams and away in teams:
                    return match

        except Exception as e:
            print("ODDS API ERROR:", e)

    return None