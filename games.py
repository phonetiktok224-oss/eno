# =========================
# 🎮 GAMES ENGINE
# =========================
import random
from ai_engine import analyse_match
from data_sources import get_all_matches

# =========================
# 🔒 SAFE MATCHES
# =========================
def safe_matches():
    try:
        m = get_all_matches()
        if m:
            return m[:8]
    except:
        pass

    return [
        {"home": "PSG", "away": "Marseille"},
        {"home": "Barcelone", "away": "Real Madrid"},
        {"home": "Chelsea", "away": "Liverpool"},
        {"home": "Bayern", "away": "Dortmund"},
        {"home": "Inter", "away": "Milan"},
        {"home": "Arsenal", "away": "City"},
        {"home": "Napoli", "away": "Roma"},
    ]

# =========================
# 🔥 TOP 3
# =========================
def top3_games():
    matches = safe_matches()
    results = []

    for m in matches:
        res = analyse_match(m["home"], m["away"])

        choice = random.choice([
            "🏆 Victoire",
            "⚽ BTTS",
            "📉 Under/Over"
        ])

        txt = f"{m['home']} vs {m['away']}\n👉 {choice} ({res['confidence']}%)"
        results.append((res["confidence"], txt))

    results.sort(reverse=True)
    return [r[1] for r in results[:3]]

# =========================
# 💎 VIP
# =========================
def vip_games():
    matches = safe_matches()
    results = []

    for m in matches:
        res = analyse_match(m["home"], m["away"])

        options = [
            "📊 Corner +",
            "🟨 Cartons +",
            "📍 Touches +"
        ]

        picks = random.sample(options, 2)

        txt = f"""
{m['home']} vs {m['away']}
👉 {picks[0]}
👉 {picks[1]}

📊 Analyse: {res['prediction']}
🔥 Confiance: {res['confidence']}%
"""
        results.append((res["confidence"], txt))

    results.sort(reverse=True)
    return [r[1] for r in results[:8]]

# =========================
# 👑 ADMIN VIP
# =========================
def admin_vip_games():
    matches = safe_matches()
    results = []

    admin_options = [
        "🚫 Pas de penalty",
        "🚫 Pas de carton rouge",
        "⚽ Favori 1-3 buts",
        "⏱️ Pas de but avant 20 min",
        "🎯 Score exact"
    ]

    for m in matches:
        res = analyse_match(m["home"], m["away"])

        picks = random.sample(admin_options, 2)

        txt = f"""
👑 {m['home']} vs {m['away']}
👉 {picks[0]}
👉 {picks[1]}

🎯 Score exact: {res['score']}
🔥 Confiance: {res['confidence']}%
"""
        results.append((res["confidence"], txt))

    results.sort(reverse=True)
    return [r[1] for r in results[:8]]

# =========================
# 🎯 SCORE EXACT VIP
# =========================
def score_exact_vip():
    matches = safe_matches()
    results = []

    for m in matches:
        res = analyse_match(m["home"], m["away"])

        txt = f"""
{m['home']} vs {m['away']}
🎯 Score exact: {res['score']}
🔥 {res['confidence']}%
"""
        results.append((res["confidence"], txt))

    results.sort(reverse=True)
    return [r[1] for r in results[:3]]
