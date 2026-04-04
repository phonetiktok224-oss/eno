import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

SPORTMONKS_KEY = os.getenv("SPORTMONKS_KEY")
FOOTBALL_DATA_KEY = os.getenv("FOOTBALL_DATA_KEY")
API_FOOTBALL_KEY = os.getenv("API_KEY")

# =========================
# 🔥 SPORTMONKS
# =========================
def get_sportmonks_matches():
    if not SPORTMONKS_KEY:
        return []

    try:
        url = f"https://api.sportmonks.com/v3/football/fixtures?api_token={SPORTMONKS_KEY}"
        res = requests.get(url).json()

        matches = []
        for m in res.get("data", []):
            matches.append({
                "home": m["participants"][0]["name"],
                "away": m["participants"][1]["name"]
            })

        return matches

    except Exception as e:
        print("SportMonks error:", e)
        return []

# =========================
# 🔥 FOOTBALL-DATA
# =========================
def get_football_data_matches():
    if not FOOTBALL_DATA_KEY:
        return []

    try:
        url = "https://api.football-data.org/v4/matches"
        headers = {"X-Auth-Token": FOOTBALL_DATA_KEY}

        res = requests.get(url, headers=headers).json()

        matches = []
        for m in res.get("matches", []):
            matches.append({
                "home": m["homeTeam"]["name"],
                "away": m["awayTeam"]["name"]
            })

        return matches

    except Exception as e:
        print("Football-Data error:", e)
        return []

# =========================
# 🔥 API-FOOTBALL (EXISTANT)
# =========================
def get_api_football_matches():
    if not API_FOOTBALL_KEY:
        return []

    today = datetime.today().strftime('%Y-%m-%d')
    tomorrow = (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')

    try:
        url = f"https://v3.football.api-sports.io/fixtures?from={today}&to={tomorrow}"
        headers = {"x-apisports-key": API_FOOTBALL_KEY}

        res = requests.get(url, headers=headers).json()

        matches = []
        for m in res.get("response", []):
            matches.append({
                "home": m["teams"]["home"]["name"],
                "away": m["teams"]["away"]["name"]
            })

        return matches

    except Exception as e:
        print("API-Football error:", e)
        return []

# =========================
# 🔥 FUSION INTELLIGENTE
# =========================
def get_all_matches():
    all_matches = []

    sources = [
        get_api_football_matches(),
        get_sportmonks_matches(),
        get_football_data_matches()
    ]

    for source in sources:
        all_matches.extend(source)

    # 🔥 SUPPRIMER DOUBLONS
    unique = []
    seen = set()

    for m in all_matches:
        key = f"{m['home']} vs {m['away']}"
        if key not in seen:
            seen.add(key)
            unique.append(m)

    print(f"✅ TOTAL MATCHES: {len(unique)}")

    return unique