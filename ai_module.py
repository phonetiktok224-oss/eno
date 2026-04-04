# ai_module.py

user_data = {}
AI_ENABLED = True

def toggle_ai(state):
    global AI_ENABLED
    AI_ENABLED = state

def log_action(user_id, action):
    if user_id not in user_data:
        user_data[user_id] = []

    user_data[user_id].append(action)

def suggest_action(user_id):
    if not AI_ENABLED:
        return None

    actions = user_data.get(user_id, [])

    if actions.count("analyse") > actions.count("matchs"):
        return "📊 Tu sembles aimer les analyses. Essaie /analyse_vip"
    else:
        return "⚽ Essaie /matchs pour voir les matchs"