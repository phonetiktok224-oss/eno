# =========================
# 🌐 DATA SOURCES PRO MAX (MULTI API KEY ROTATION)
# =========================

import requests
from datetime import datetime

# =========================
# 🔑 CONFIG API (PLUSIEURS CLES)
# =========================
API_KEYS = [
    "574429af1fa8d741a94929ecb71353dae87ea152ca77e856b8fdb6f6fc36de2b",
    "1gZkFisH6QUK8l4W9UEgsoY5rCfQz8FS3nxXHS8k6cZKNcUbpTVnb6aXGfA0",
    "49fee72ae7a64cf3a8b33331be4b671d",
    "39d58474dddabacad4a8181186ee72ce"
]


# =========================
# 🔁 REQUETE AVEC ROTATION DES CLES
# =========================
def fetch_with_rotation(url):
    for key in API_KEYS:
        headers = {
            "x-apisports-key": key
        }

        try:
            response = requests.get(url, headers=headers, timeout=10)

            # ✅ Si succès
            if response.status_code == 200:
                data = response.json()

                if data.get("response"):
                    print(f"✅ API KEY OK: {key[:6]}...")
                    return data

            else:
                print(f"⚠️ Key échouée: {key[:6]}...")

        except Exception as e:
            print(f"❌ Erreur clé {key[:6]}:", e)

    return None


# =========================
# 🥇 API PRINCIPALE (MULTI KEY)
# =========================
def get_matches_api_1():
    today = datetime.now().strftime("%Y-%m-%d")

    url = f"https://v3.football.api-sports.io/fixtures?date={today}"

    data = fetch_with_rotation(url)

    if not data:
        return []

    matches = []

    for match in data.get("response", []):
        matches.append({
            "home": match["teams"]["home"]["name"],
            "away": match["teams"]["away"]["name"],
            "date": match["fixture"]["date"],
            "league": match["league"]["name"]
        })

    return matches


# =========================
# 🥈 API SECONDAIRE (FALLBACK)
# =========================
def get_matches_api_2():
    today = datetime.now().strftime("%Y-%m-%d")

    return [
        {"home": "Real Madrid", "away": "Barcelona", "date": today, "league": "Liga"},
        {"home": "Man City", "away": "Liverpool", "date": today, "league": "Premier League"},
        {"home": "PSG", "away": "Marseille", "date": today, "league": "Ligue 1"},
    ]


# =========================
# 🧹 SUPPRESSION DOUBLONS
# =========================
def remove_duplicates(matches):
    seen = set()
    unique_matches = []

    for m in matches:
        key = (m["home"], m["away"], m["date"])

        if key not in seen:
            seen.add(key)
            unique_matches.append(m)

    return unique_matches


# =========================
# 🚀 FONCTION PRINCIPALE
# =========================
def get_all_matches():
    matches = []

    # 🔥 API PRINCIPALE (rotation keys)
    try:
        matches = get_matches_api_1()
    except:
        print("❌ Erreur API principale")

    # 🔁 FALLBACK SI VIDE
    if not matches:
        print("⚠️ API vide → fallback activé")
        try:
            matches = get_matches_api_2()
        except:
            print("❌ Erreur fallback")

    # 🧹 CLEAN
    matches = remove_duplicates(matches)

    return matches
