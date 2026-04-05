# =========================
# 🌐 DATA SOURCES PRO MAX (MULTI API + SECURE)
# =========================

import requests
from datetime import datetime

API_KEYS = [
    "574429af1fa8d741a94929ecb71353dae87ea152ca77e856b8fdb6f6fc36de2b",
    "39d58474dddabacad4a8181186ee72ce",
    "2148a5436bff4a92832aa2d5d8ff1882"
]

# =========================
# 🔁 ROTATION API KEYS
# =========================
def fetch_api(url):
    for key in API_KEYS:
        try:
            headers = {"x-apisports-key": key}
            res = requests.get(url, headers=headers, timeout=10)

            if res.status_code == 200:
                data = res.json()
                if data.get("response"):
                    return data

        except Exception as e:
            print("❌ API error:", e)

    return None


# =========================
# 📡 API FOOTBALL
# =========================
def get_matches_api():
    today = datetime.now().strftime("%Y-%m-%d")

    url = f"https://v3.football.api-sports.io/fixtures?date={today}"
    data = fetch_api(url)

    if not data:
        return []

    matches = []

    for m in data.get("response", []):
        matches.append({
            "home": m["teams"]["home"]["name"],
            "away": m["teams"]["away"]["name"],
            "league": m["league"]["name"],
            "date": m["fixture"]["date"]
        })

    return matches


# =========================
# 🔁 FALLBACK
# =========================
def fallback_matches():
    today = datetime.now().strftime("%Y-%m-%d %H:%M")

    return [
        {"home": "Real Madrid", "away": "Barcelona", "league": "Liga", "date": today},
        {"home": "PSG", "away": "Marseille", "league": "Ligue 1", "date": today}
    ]


# =========================
# 🧹 CLEAN
# =========================
def clean(matches):
    seen = set()
    final = []

    for m in matches:
        key = (m["home"], m["away"], m["date"])
        if key not in seen:
            seen.add(key)
            final.append(m)

    return final


# =========================
# 🚀 MAIN
# =========================
def get_all_matches():
    matches = get_matches_api()

    if not matches:
        print("⚠️ fallback utilisé")
        matches = fallback_matches()

    return clean(matches)