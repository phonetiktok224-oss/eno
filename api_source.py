import requests
from datetime import datetime

API_KEY = "39d58474dddabacad4a8181186ee72ce"

def get_matches_api():
    today = datetime.now().strftime("%Y-%m-%d")

    url = f"https://v3.football.api-sports.io/fixtures?date={today}"

    headers = {
        "x-apisports-key": API_KEY
    }

    try:
        response = requests.get(url, headers=headers)
        data = response.json()

        matches = []

        for match in data.get("response", []):
            matches.append({
                "home": match["teams"]["home"]["name"],
                "away": match["teams"]["away"]["name"],
                "date": match["fixture"]["date"],
                "league": match["league"]["name"]
            })

        return matches

    except Exception as e:
        print("Erreur API :", e)
        return []
