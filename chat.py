# chat.py

def generate_reply(message):
    msg = message.lower()

    if "bonjour" in msg:
        return "👋 Bonjour !"

    if "vip" in msg:
        return "💎 Deviens VIP avec /devenir_vip"

    if "match" in msg:
        return "⚽ Tape /matchs"

    return "🤖 Utilise /analyse ou /matchs"