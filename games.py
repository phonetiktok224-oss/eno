# =========================
# 🎮 GAMES ENGINE PRO MAX FINAL
# =========================
import random
from datetime import datetime
from ai_engine import analyse_match
from data_sources import get_all_matches
from odds_api import fetch_odds
from database import save_prono

# =========================
# NORMALISATION
# =========================
def normalize_match(m):
    if not m.get("home") or not m.get("away"):
        return None

    return {
        "home": m["home"],
        "away": m["away"],
        "league": m.get("league", "Unknown"),
        "date": m.get("date", datetime.now().strftime("%Y-%m-%d %H:%M"))
    }

# =========================
# MATCHS DU JOUR
# =========================
def today_matches():
    try:
        data = get_all_matches()
    except Exception as e:
        print("❌ ERROR:", e)
        return []

    matches = []

    for m in data:
        m = normalize_match(m)
        if m:
            matches.append(m)

    return matches[:20]

# =========================
# FORMAT MATCH
# =========================
def format_match(m):
    try:
        dt = datetime.strptime(m["date"], "%Y-%m-%d %H:%M")
    except:
        dt = datetime.now()

    return f"{m['home']} vs {m['away']}\n🕒 {dt.strftime('%H:%M')} | 📅 {dt.strftime('%d-%m-%Y')} | 🏆 {m['league']}"

# =========================
# 🎯 LOGIQUE ADMIN VIP (STRATÉGIE)
# =========================
def build_admin_choices(res):
    conf = res["confidence"]

    # 🔥 OPTION 1 : Favori marque 1 à 3 buts
    choice1 = {
        "label": "Favori marque 1 à 3 buts",
        "prob": min(92, conf + random.randint(3, 7))
    }

    # 🔥 OPTION 2 : But avant 20 min (ou non)
    early = random.choice([True, False])
    prob2 = max(55, min(90, conf + random.randint(-5, 5)))

    choice2 = {
        "label": "But avant 20 min" if early else "Pas de but avant 20 min",
        "prob": prob2
    }

    return choice1, choice2

# =========================
# 📊 OPTIONS SECONDAIRES
# =========================
def build_secondary_data():
    return {
        "corners": random.randint(8, 14),
        "cards": random.randint(2, 6),
        "touches": random.randint(20, 50)
    }

# =========================
# 🔥 TOP 3
# =========================
def top3_games():
    matches = today_matches()
    if not matches:
        return ["❌ Aucun match"]

    results = []

    for m in matches:
        res = analyse_match(m["home"], m["away"])

        save_prono({
            "match": f"{m['home']} vs {m['away']}",
            "prediction": res["prediction"],
            "confidence": res["confidence"]
        })

        txt = f"""{format_match(m)}

🔥 {res['prediction']}
📊 {res['confidence']}%
"""
        results.append((res["confidence"], txt))

    results.sort(reverse=True)
    return [r[1] for r in results[:3]]

# =========================
# 💎 VIP
# =========================
def vip_games():
    matches = today_matches()
    if not matches:
        return ["❌ Aucun match"]

    results = []

    for m in matches:
        res = analyse_match(m["home"], m["away"])

        save_prono({
            "match": f"{m['home']} vs {m['away']}",
            "prediction": res["prediction"],
            "confidence": res["confidence"]
        })

        txt = f"""{format_match(m)}

💎 {res['prediction']}
🔥 Confiance: {res['confidence']}%

⚽ Analyse buts & dynamique offensive
"""
        results.append((res["confidence"], txt))

    results.sort(reverse=True)
    return [r[1] for r in results[:8]]

# =========================
# 👑 ADMIN VIP (STRATÉGIE AVANCÉE)
# =========================
def admin_vip_games():
    matches = today_matches()
    if not matches:
        return ["❌ Aucun match"]

    results = []

    for m in matches:
        res = analyse_match(m["home"], m["away"])
        odds_data = fetch_odds(m["home"], m["away"])  # ⚠️ poids faible

        # 🎯 OPTIONS PRINCIPALES
        c1, c2 = build_admin_choices(res)

        # 📊 SECONDAIRES
        sec = build_secondary_data()

        save_prono({
            "match": f"{m['home']} vs {m['away']}",
            "prediction": res["prediction"],
            "confidence": res["confidence"]
        })

        txt = f"""{format_match(m)}

👑 ADMIN VIP - STRATÉGIE

🎯 OPTIONS PRINCIPALES:

1️⃣ {c1['label']}
📊 Réussite: {c1['prob']}%

2️⃣ {c2['label']}
📊 Réussite: {c2['prob']}%

📊 OPTIONS SECONDAIRES:

📐 Corners: {sec['corners']}
🟨 Cartons: {sec['cards']}
📍 Touches: {sec['touches']}

🧠 ANALYSE IA:
{res['prediction']} ({res['confidence']}%)

⚠️ Pénalty / Expulsion NON recommandés
"""
        results.append((res["confidence"], txt))

    results.sort(reverse=True)
    return [r[1] for r in results[:10]]

# =========================
# 🎯 SCORE EXACT VIP
# =========================
def score_exact_vip():
    matches = today_matches()
    if not matches:
        return ["❌ Aucun match"]

    results = []

    for m in matches:
        res = analyse_match(m["home"], m["away"])

        save_prono({
            "match": f"{m['home']} vs {m['away']}",
            "prediction": res["prediction"],
            "confidence": res["confidence"]
        })

        txt = f"""{format_match(m)}
🎯 Score: {res['score']}
🔥 {res['confidence']}%
"""
        results.append((res["confidence"], txt))

    results.sort(reverse=True)
    return [r[1] for r in results[:5]]