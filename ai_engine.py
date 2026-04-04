import random

def analyse_match(home, away, stats=None):

    # =========================
    # 📊 STATS SIMULÉES (API READY)
    # =========================
    GP = random.randint(10, 30)
    W = random.randint(40, 80)
    BTS = random.randint(40, 80)
    GF = round(random.uniform(0.8, 2.5), 2)
    GA = round(random.uniform(0.5, 2.0), 2)
    OVER25 = random.randint(40, 75)

    # =========================
    # 🎯 LOGIQUE PRO
    # =========================
    total = GF + GA

    if W > 60 and GF > 1.5:
        prediction = f"{home} gagne"
        bet_type = "🏆 Victoire domicile"
    elif BTS > 60:
        prediction = "BTTS OUI"
        bet_type = "⚽ Les deux équipes marquent"
    elif total < 2.5:
        prediction = "Moins de 2.5 buts"
        bet_type = "🔒 Match fermé"
    else:
        prediction = "Plus de 1.5 buts"
        bet_type = "🔥 Match ouvert"

    # =========================
    # 🎯 SCORE EXACT
    # =========================
    if total < 2:
        score = "1-0"
    elif total < 3:
        score = "2-0 / 1-1"
    else:
        score = "2-1 / 3-1"

    # =========================
    # 🔥 CONFIANCE
    # =========================
    confidence = int((W + BTS + OVER25) / 3)

    # =========================
    # 💎 VIP
    # =========================
    vip = []
    if 1 <= total <= 3:
        vip.append("⚽ 1-3 buts")
    if total < 3:
        vip.append("⏱️ Pas de but avant 20 min")
    if W > 55:
        vip.append("🚫 Pas de rouge")

    # =========================
    # 🧠 META (ADMIN ONLY)
    # =========================
    return {
        "prediction": prediction,
        "confidence": confidence,
        "type": bet_type,
        "score": score,
        "vip": vip,
        "league": "TOP" if W > 55 else "MOYEN",
        "stats": {
            "GP": GP,
            "W": W,
            "BTS": BTS,
            "GF": GF,
            "GA": GA,
            "OVER25": OVER25
        }
    }