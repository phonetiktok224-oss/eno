import os
import requests

API_KEY = os.getenv("FOOTBALL_API_KEY")

def get_matches_api():
    if not API_KEY:
        return []

    try:
        url = "https://api.football-data.org/v4/matches"
        headers = {"X-Auth-Token": API_KEY}

        res = requests.get(url, headers=headers, timeout=10)
        data = res.json()

        matches = []

        for m in data.get("matches", []):
            matches.append({
                "home": m["homeTeam"]["name"],
                "away": m["awayTeam"]["name"],
                "date": m["utcDate"][:16].replace("T", " "),
                "league": m["competition"]["name"]
            })

        return matches

    except Exception as e:
        print("API ERROR:", e)
        return []