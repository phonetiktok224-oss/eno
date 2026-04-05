# =========================
# 🎮 GAMES ENGINE FINAL PRO
# =========================
import random
from datetime import datetime
from ai_engine import analyse_match
from data_sources import get_all_matches
from odds_api import fetch_odds
from database import save_prono

def normalize_match(m):
    if not m.get("home") or not m.get("away"):
        return None

    return {
        "home": m["home"],
        "away": m["away"],
        "league": m.get("league", "Unknown"),
        "date": m.get("date", datetime.now().strftime("%Y-%m-%d %H:%M"))
    }

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

def format_match(m):
    try:
        dt = datetime.strptime(m["date"], "%Y-%m-%d %H:%M")
    except:
        dt = datetime.now()

    return f"{m['home']} vs {m['away']}\n🕒 {dt.strftime('%H:%M')} | 📅 {dt.strftime('%d-%m-%Y')} | 🏆 {m['league']}"

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
"""
        results.append((res["confidence"], txt))

    results.sort(reverse=True)
    return [r[1] for r in results[:8]]

def admin_vip_games():
    matches = today_matches()
    if not matches:
        return ["❌ Aucun match"]

    results = []

    for m in matches:
        res = analyse_match(m["home"], m["away"])
        odds_data = fetch_odds(m["home"], m["away"])

        save_prono({
            "match": f"{m['home']} vs {m['away']}",
            "prediction": res["prediction"],
            "confidence": res["confidence"]
        })

        txt = f"""{format_match(m)}

👑 ADMIN VIP

🧠 {res['prediction']}
📊 {res['confidence']}%
"""
        results.append((res["confidence"], txt))

    results.sort(reverse=True)
    return [r[1] for r in results[:10]]

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