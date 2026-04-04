# =========================
# API FOOTBALL + FALLBACK + CACHE + SPORTMONKS
# =========================
import requests
import time
import logging
import os

# =========================
# CONFIG API (RENDER READY)
# =========================
API_KEY = os.getenv("API_KEY")
BASE_URL = "https://v3.football.api-sports.io"

SPORTMONKS_API_KEY = os.getenv("SPORTMONKS_API_KEY")
SPORTMONKS_URL = "https://api.sportmonks.com/v3/football/fixtures"

HEADERS = {
    "x-apisports-key": API_KEY or ""
}

# =========================
# CACHE
# =========================
CACHE = {
    "data": [],
    "timestamp": 0
}

CACHE_DURATION = 600  # 10 minutes

# =========================
# API PRINCIPALE (API-FOOTBALL)
# =========================
def get_api_football():
    try:
        url = f"{BASE_URL}/fixtures?live=all"

        response = requests.get(url, headers=HEADERS, timeout=10)

        if response.status_code != 200:
            logging.error(f"API-Football status error: {response.status_code}")
            return []

        data = response.json()

        matches = []

        for m in data.get("response", []):
            try:
                matches.append({
                    "home": m["teams"]["home"]["name"],
                    "away": m["teams"]["away"]["name"]
                })
            except:
                continue

        return matches

    except Exception as e:
        logging.error(f"API-Football error: {e}")
        return []

# =========================
# API SECOURS 1 (FOOTBALL-DATA)
# =========================
def get_backup_api():
    try:
        url = "https://api.football-data.org/v4/matches"
        headers = {"X-Auth-Token": "demo"}

        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code != 200:
            return []

        data = response.json()

        matches = []

        for m in data.get("matches", []):
            try:
                matches.append({
                    "home": m["homeTeam"]["name"],
                    "away": m["awayTeam"]["name"]
                })
            except:
                continue

        return matches

    except Exception as e:
        logging.error(f"Football-Data error: {e}")
        return []

# =========================
# API SECOURS 2 (SPORTMONKS)
# =========================
def get_sportmonks():
    try:
        if not SPORTMONKS_API_KEY:
            return []

        url = f"{SPORTMONKS_URL}?api_token={SPORTMONKS_API_KEY}&include=participants"

        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            logging.error(f"SportMonks status error: {response.status_code}")
            return []

        data = response.json()

        matches = []

        for m in data.get("data", []):
            try:
                participants = m.get("participants", [])

                if len(participants) >= 2:
                    home = participants[0].get("name")
                    away = participants[1].get("name")

                    if home and away:
                        matches.append({
                            "home": home,
                            "away": away
                        })
            except:
                continue

        return matches

    except Exception as e:
        logging.error(f"SportMonks error: {e}")
        return []

# =========================
# FONCTION PRINCIPALE
# =========================
def get_all_matches():
    current_time = time.time()

    # 🔥 CACHE
    if CACHE["data"] and (current_time - CACHE["timestamp"] < CACHE_DURATION):
        return CACHE["data"]

    # 🥇 API PRINCIPALE
    matches = get_api_football()
    if matches:
        CACHE["data"] = matches
        CACHE["timestamp"] = current_time
        return matches

    # 🥈 BACKUP 1
    matches = get_backup_api()
    if matches:
        CACHE["data"] = matches
        CACHE["timestamp"] = current_time
        return matches

    # 🥉 BACKUP 2 (SPORTMONKS)
    matches = get_sportmonks()

    CACHE["data"] = matches
    CACHE["timestamp"] = current_time

    return matches