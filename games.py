# =========================
# 🎮 GAMES ENGINE PRO MAX
# =========================
import random
from datetime import datetime
from ai_engine import analyse_match
from data_sources import get_all_matches

# =========================
# NORMALISATION MATCHS
# =========================
def normalize_match(m):
    return {
        "home": m.get("home", "Team A"),
        "away": m.get("away", "Team B"),
        "league": m.get("league", "Unknown"),
        "date": m.get("date", datetime.utcnow().strftime("%Y-%m-%d %H:%M"))
    }

# =========================
# MATCHS DU JOUR
# =========================
def today_matches():
    matches = []

    try:
        for m in get_all_matches():
            m = normalize_match(m)
            matches.append(m)

        if matches:
            return matches[:15]

    except:
        pass

    # fallback solide
    return [
        {"home": "PSG", "away": "Marseille", "league": "Ligue 1", "date": "2026-04-05 20:00"},
        {"home": "Barcelona", "away": "Real Madrid", "league": "La Liga", "date": "2026-04-05 21:00"},
    ]

# =========================
# 📊 COTES BOOKMAKER
# =========================
def generate_odds(confidence):
    base = round(100 / max(confidence, 50), 2)

    return {
        "home_win": round(base, 2),
        "draw": round(base + 0.8, 2),
        "away_win": round(base + 1.2, 2),
        "over25": round(base - 0.3, 2),
        "btts": round(base - 0.5, 2)
    }

# =========================
# FORMAT
# =========================
def format_match(m):
    dt = datetime.strptime(m["date"], "%Y-%m-%d %H:%M")
    return f"{m['home']} vs {m['away']}\n🕒 {dt.strftime('%H:%M')} | 📅 {dt.strftime('%d-%m-%Y')} | 🏆 {m['league']}"

# =========================
# 🔥 TOP 3
# =========================
def top3_games():
    results = []

    for m in today_matches():
        res = analyse_match(m["home"], m["away"])
        odds = generate_odds(res["confidence"])

        txt = f"""{format_match(m)}

🔥 Choix: {res['prediction']}
📊 Confiance: {res['confidence']}%

💰 Cotes:
🏠 {odds['home_win']} | 🤝 {odds['draw']} | 🛫 {odds['away_win']}
"""
        results.append((res["confidence"], txt))

    results.sort(reverse=True)
    return [r[1] for r in results[:3]]

# =========================
# 💎 VIP
# =========================
def vip_games():
    results = []

    for m in today_matches():
        res = analyse_match(m["home"], m["away"])
        odds = generate_odds(res["confidence"])

        txt = f"""{format_match(m)}

📊 Analyse: {res['prediction']}
💎 Confiance: {res['confidence']}%

💰 Over 2.5: {odds['over25']}
⚽ BTTS: {odds['btts']}
"""
        results.append((res["confidence"], txt))

    results.sort(reverse=True)
    return [r[1] for r in results[:8]]

# =========================
# 👑 ADMIN VIP = BOOKMAKER 😈
# =========================
def admin_vip_games():
    results = []

    for m in today_matches():
        res = analyse_match(m["home"], m["away"])
        odds = generate_odds(res["confidence"])

        txt = f"""{format_match(m)}

👑 BOOKMAKER MODE

📊 Prédiction: {res['prediction']}
🔥 Confiance: {res['confidence']}%

💰 MARCHÉS:

🏆 1X2:
- Victoire domicile: {odds['home_win']}
- Nul: {odds['draw']}
- Extérieur: {odds['away_win']}

⚽ BUTS:
- Over 2.5: {odds['over25']}
- BTTS: {odds['btts']}

🎯 SCORE EXACT:
→ {res['score']}

🧠 STRATÉGIE:
Match exploitable avec avantage statistique clair
"""
        results.append((res["confidence"], txt))

    results.sort(reverse=True)
    return [r[1] for r in results[:10]]

# =========================
# 🎯 SCORE EXACT
# =========================
def score_exact_vip():
    results = []

    for m in today_matches():
        res = analyse_match(m["home"], m["away"])

        txt = f"""{format_match(m)}
🎯 Score: {res['score']}
🔥 {res['confidence']}%
"""
        results.append((res["confidence"], txt))

    results.sort(reverse=True)
    return [r[1] for r in results[:5]]
