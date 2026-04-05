# =========================
# 🤖 AI ENGINE PRO
# =========================
import random

def analyse_match(home, away):
    attack_home = random.uniform(0.8, 1.5)
    attack_away = random.uniform(0.8, 1.5)

    defense_home = random.uniform(0.8, 1.5)
    defense_away = random.uniform(0.8, 1.5)

    home_score = attack_home / defense_away
    away_score = attack_away / defense_home

    home_goals = min(4, int(home_score * 2))
    away_goals = min(4, int(away_score * 2))

    if home_goals > away_goals:
        prediction = f"{home} gagne"
    elif away_goals > home_goals:
        prediction = f"{away} gagne"
    else:
        prediction = "Match nul"

    confidence = int(60 + abs(home_goals - away_goals) * 10 + random.randint(0, 10))

    return {
        "prediction": prediction,
        "confidence": min(95, confidence),
        "score": f"{home_goals}-{away_goals}"
    }