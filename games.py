# =========================
# 🎮 GAMES ENGINE PRO+
# =========================
import random
from datetime import datetime
from ai_engine import analyse_match
from data_sources import get_all_matches

# =========================
# 📅 MATCHS DU JOUR
# =========================
def today_matches():
    today = datetime.utcnow().date()
    matches = []

    try:
        all_matches = get_all_matches()

        for m in all_matches:
            if "date" in m:
                match_date = datetime.strptime(m["date"], "%Y-%m-%d %H:%M").date()
                if match_date == today:
                    matches.append(m)

        if matches:
            return matches[:10]

    except:
        pass

    # fallback si API vide
    return [
        {"home": "PSG", "away": "Marseille", "league": "Ligue 1", "date": "2026-04-05 20:00"},
        {"home": "Barcelone", "away": "Real Madrid", "league": "La Liga", "date": "2026-04-05 21:00"},
    ]

# =========================
# 📊 STATS
# =========================
def generate_stats():
    return {
        "corners_avg": random.randint(7, 10),
        "corners_max": random.randint(11, 15),
        "cards_avg": random.randint(2, 5),
        "cards_max": random.randint(6, 10),
        "touches_avg": random.randint(20, 35),
        "touches_max": random.randint(40, 60),
    }

def format_match(m):
    dt = datetime.strptime(m["date"], "%Y-%m-%d %H:%M")
    return f"{m['home']} vs {m['away']}\n🕒 {dt.strftime('%H:%M')} | 📅 {dt.strftime('%d-%m-%Y')} | 🏆 {m.get('league','N/A')}"

# =========================
# 🔥 TOP 3
# =========================
def top3_games():
    matches = today_matches()
    results = []

    for m in matches:
        res = analyse_match(m["home"], m["away"])
        base = format_match(m)

        txt = f"""{base}
🔥 Choix: Victoire / BTTS
📊 Confiance: {res['confidence']}%
"""
        results.append((res["confidence"], txt))

    results.sort(reverse=True)
    return [r[1] for r in results[:3]]

# =========================
# 💎 VIP
# =========================
def vip_games():
    matches = today_matches()
    results = []

    for m in matches:
        res = analyse_match(m["home"], m["away"])
        stats = generate_stats()
        base = format_match(m)

        txt = f"""{base}

📊 Corners: {stats['corners_avg']} (max {stats['corners_max']})
🟨 Cartons: {stats['cards_avg']} (max {stats['cards_max']})
📍 Touches: {stats['touches_avg']} (max {stats['touches_max']})

🔥 Analyse: {res['prediction']}
💎 Confiance: {res['confidence']}%
"""
        results.append((res["confidence"], txt))

    results.sort(reverse=True)
    return [r[1] for r in results[:8]]

# =========================
# 👑 ADMIN VIP
# =========================
def admin_vip_games():
    matches = today_matches()
    results = []

    for m in matches:
        res = analyse_match(m["home"], m["away"])
        stats = generate_stats()
        base = format_match(m)

        txt = f"""{base}

👑 MODE ADMIN

📊 Corners: {stats['corners_avg']} → max {stats['corners_max']}
🟨 Cartons: {stats['cards_avg']} → max {stats['cards_max']}
📍 Touches: {stats['touches_avg']} → max {stats['touches_max']}

🎯 Score exact: {res['score']}
🔥 Confiance MAX: {res['confidence']}%
"""
        results.append((res["confidence"], txt))

    results.sort(reverse=True)
    return [r[1] for r in results[:8]]

# =========================
# 🎯 SCORE EXACT VIP
# =========================
def score_exact_vip():
    matches = today_matches()
    results = []

    for m in matches:
        res = analyse_match(m["home"], m["away"])
        base = format_match(m)

        txt = f"""{base}
🎯 Score exact: {res['score']}
🔥 {res['confidence']}%
"""
        results.append((res["confidence"], txt))

    results.sort(reverse=True)
    return [r[1] for r in results[:3]]
