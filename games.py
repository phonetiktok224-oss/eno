# =========================
# 🎮 GAMES ENGINE FINAL PRO
# =========================
import random
from datetime import datetime
from ai_engine import analyse_match
from data_sources import get_all_matches
from odds_api import fetch_odds

# =========================
# NORMALISATION
# =========================
def normalize_match(m):
    if not m.get("home") or not m.get("away") or not m.get("date"):
        return None

    return {
        "home": m["home"],
        "away": m["away"],
        "league": m.get("league", "Unknown"),
        "date": m["date"]
    }

# =========================
# MATCHS API ONLY
# =========================
def today_matches():
    matches = []

    try:
        data = get_all_matches()

        for m in data:
            m = normalize_match(m)
            if m:
                matches.append(m)

    except Exception as e:
        print("❌ MATCH API ERROR:", e)
        return []

    return matches[:20]

# =========================
# FORMAT
# =========================
def format_match(m):
    dt = datetime.strptime(m["date"], "%Y-%m-%d %H:%M")
    return f"{m['home']} vs {m['away']}\n🕒 {dt.strftime('%H:%M')} | 📅 {dt.strftime('%d-%m-%Y')} | 🏆 {m['league']}"

# =========================
# ADMIN LOGIQUE
# =========================
def build_admin_choices(res, odds_data=None):
    conf = res["confidence"]

    boost = 0
    if odds_data:
        boost = random.randint(1, 3)  # < 10%

    choice1 = {
        "label": "Favori marque 1 à 3 buts",
        "prob": min(92, conf + boost + random.randint(2, 6))
    }

    early_goal = random.choice([True, False])

    choice2 = {
        "label": "But avant 20 min" if early_goal else "Pas de but avant 20 min",
        "prob": max(55, min(90, conf + boost + random.randint(-3, 4)))
    }

    return choice1, choice2

# =========================
# TOP 3
# =========================
def top3_games():
    matches = today_matches()

    if not matches:
        return ["❌ Aucun match disponible (API)"]

    results = []

    for m in matches:
        res = analyse_match(m["home"], m["away"])

        txt = f"""{format_match(m)}

🔥 {res['prediction']}
📊 {res['confidence']}%
"""
        results.append((res["confidence"], txt))

    results.sort(reverse=True)
    return [r[1] for r in results[:3]]

# =========================
# VIP
# =========================
def vip_games():
    matches = today_matches()

    if not matches:
        return ["❌ Aucun match API"]

    results = []

    for m in matches:
        res = analyse_match(m["home"], m["away"])

        txt = f"""{format_match(m)}

💎 {res['prediction']}
🔥 Confiance: {res['confidence']}%
"""
        results.append((res["confidence"], txt))

    results.sort(reverse=True)
    return [r[1] for r in results[:8]]

# =========================
# ADMIN VIP
# =========================
def admin_vip_games():
    matches = today_matches()

    if not matches:
        return ["❌ Aucun match API"]

    results = []

    for m in matches:
        res = analyse_match(m["home"], m["away"])

        odds_data = fetch_odds(m["home"], m["away"])

        c1, c2 = build_admin_choices(res, odds_data)

        corners = random.randint(8, 13)
        cards = random.randint(3, 6)
        touches = random.randint(20, 45)

        txt = f"""{format_match(m)}

👑 ADMIN VIP PRO

🎯 OPTIONS PRINCIPALES

1️⃣ {c1['label']}
📊 {c1['prob']}%

2️⃣ {c2['label']}
📊 {c2['prob']}%

📊 OPTIONS SECONDAIRES

📐 Corners: {corners}
🟨 Cartons: {cards}
📍 Touches: {touches}

🧠 IA: {res['prediction']} ({res['confidence']}%)

⚠️ Pénalty / Expulsion exclus
"""
        results.append((res["confidence"], txt))

    results.sort(reverse=True)
    return [r[1] for r in results[:10]]

# =========================
# SCORE EXACT
# =========================
def score_exact_vip():
    matches = today_matches()

    if not matches:
        return ["❌ Aucun match API"]

    results = []

    for m in matches:
        res = analyse_match(m["home"], m["away"])

        txt = f"""{format_match(m)}
🎯 Score: {res['score']}
🔥 {res['confidence']}%
"""
        results.append((res["confidence"], txt))

    results.sort(reverse=True)
    return [r[1] for r in results[:5]]
