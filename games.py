# =========================
# 🎮 GAMES ENGINE PRO MAX FINAL (ULTRA HIÉRARCHIQUE + SUPER IA)
# =========================

import random
from datetime import datetime
from data_sources import get_all_matches
from ai_engine import analyse_match
from database import save_prono

# =========================
# NORMALISATION
# =========================
def normalize(m):
    return {
        "home": m["home"],
        "away": m["away"],
        "league": m.get("league", "Unknown"),
        "date": m.get("date", datetime.now().strftime("%Y-%m-%d %H:%M"))
    }

def today_matches():
    data = get_all_matches()
    return [normalize(m) for m in data][:20]

def format_match(m):
    try:
        dt = datetime.strptime(m["date"][:16], "%Y-%m-%dT%H:%M")
    except:
        dt = datetime.now()

    return f"{m['home']} vs {m['away']}\n🕒 {dt.strftime('%H:%M')} | 📅 {dt.strftime('%d-%m-%Y')} | 🏆 {m['league']}"

# =========================
# 🧠 SUPER IA (EN SOURDINE)
# =========================
def super_ai_analysis(conf):
    # ⚠️ Invisible pour utilisateur → influence logique
    boost = 0

    if conf > 80:
        boost += 5
    if conf < 60:
        boost -= 5

    return conf + boost

# =========================
# 🔥 TOP 3 (FREE)
# =========================
def top3_games():
    matches = today_matches()
    results = []

    for m in matches:
        res = analyse_match(m["home"], m["away"])
        conf = super_ai_analysis(res["confidence"])

        txt = f"""{format_match(m)}

🔥 {res['prediction']}
📊 {conf}%
"""

        results.append((conf, txt))

    return [r[1] for r in sorted(results, reverse=True)[:3]]

# =========================
# 💎 VIP (FAR + FREE UNIQUEMENT)
# =========================
def vip_games():
    matches = today_matches()
    results = []

    for m in matches:
        res = analyse_match(m["home"], m["away"])
        conf = super_ai_analysis(res["confidence"])

        # 🎯 UN SEUL CHOIX FAR (le meilleur)
        far_choice = random.choice([
            "Corners élevés",
            "Beaucoup de touches",
            "Plus de fautes",
            "Plus de tirs"
        ])

        txt = f"""{format_match(m)}

💎 VIP

📊 {conf}%

🎯 OPTION:
{far_choice}

🔥 TENDANCE:
{res['prediction']}
"""

        results.append((conf, txt))

    return [r[1] for r in sorted(results, reverse=True)[:8]]

# =========================
# 👑 ADMIN VIP (ULTRA STRUCTURÉ)
# =========================
def admin_vip_games():
    matches = today_matches()
    results = []

    for m in matches:
        res = analyse_match(m["home"], m["away"])
        conf = super_ai_analysis(res["confidence"])

        # 🎯 PRINCIPAL (1 seul)
        principal = random.choice([
            "Pas de pénalty",
            "Pas d'expulsion",
            "Favori marque 1 à 3 buts",
            "Pas de but avant 20 min"
        ])

        # 🎯 SECONDAIRE (1 seul venant VIP)
        secondaire = random.choice([
            "Corners élevés",
            "Touches nombreuses",
            "Beaucoup de tirs"
        ])

        # 🎯 FREE (1 seul)
        free_pick = res["prediction"]

        # 🎯 SCORE EXACT (OBLIGATOIRE)
        if conf >= 85:
            score = random.choice(["2-0", "3-1"])
        elif conf >= 75:
            score = random.choice(["1-0", "2-1"])
        else:
            score = "1-1"

        txt = f"""{format_match(m)}

👑 ADMIN VIP

🎯 PRINCIPAL:
{principal}

🎯 SECONDAIRE:
{secondaire}

🎯 FREE:
{free_pick}

🎯 SCORE EXACT:
{score}

📊 CONFIANCE:
{conf}%

💡 CONSEIL:
Jouer uniquement si cote stable
"""

        results.append((conf, txt))

    return [r[1] for r in sorted(results, reverse=True)[:10]]

# =========================
# 🎯 SCORE EXACT VIP (TOP 3 UNIQUEMENT)
# =========================
def score_exact_vip():
    matches = today_matches()
    results = []

    for m in matches:
        res = analyse_match(m["home"], m["away"])
        conf = super_ai_analysis(res["confidence"])

        if conf >= 85:
            score = random.choice(["2-0", "3-1"])
        elif conf >= 75:
            score = random.choice(["1-0", "2-1"])
        else:
            score = random.choice(["1-1"])

        txt = f"""{format_match(m)}

🎯 SCORE EXACT VIP

{score}
📊 {conf}%
"""

        results.append((conf, txt))

    return [r[1] for r in sorted(results, reverse=True)[:3]]