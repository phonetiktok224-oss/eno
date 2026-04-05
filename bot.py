import os
import logging
from dotenv import load_dotenv

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

from subscription import check_sub, add_sub
from database import *
from games import *

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = str(os.getenv("ADMIN_ID"))

logging.basicConfig(level=logging.INFO)

def is_admin(uid):
    return str(uid) == ADMIN_ID

def is_vip(uid):
    return check_sub(uid) or is_vip_db(uid)

keyboard = [
    ["🔥 TOP 3", "💎 VIP"],
    ["🎯 SCORE EXACT VIP", "👑 ADMIN VIP"],
    ["💳 PAYER VIP", "📊 INFOS MATCH"],
    ["🤖 AUTO PRONO", "📊 DASHBOARD"],
    ["📜 HISTORIQUE"]
]

markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 BOT PRO MAX ACTIF", reply_markup=markup)

async def addvip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return
    try:
        uid = context.args[0]
        add_sub(uid)
        add_vip_db(uid)
        await update.message.reply_text(f"✅ VIP ajouté: {uid}")
    except:
        await update.message.reply_text("❌ /addvip USER_ID")

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    uid = str(update.effective_user.id)

    if text == "🔥 TOP 3":
        return await update.message.reply_text("\n\n".join(top3_games()))

    elif text == "💎 VIP":
        if not is_vip(uid):
            return await update.message.reply_text("⛔ VIP requis")
        return await update.message.reply_text("\n\n".join(vip_games()))

    elif text == "👑 ADMIN VIP":
        if not is_admin(uid):
            return await update.message.reply_text("⛔ Admin uniquement")
        return await update.message.reply_text("\n\n".join(admin_vip_games()))

    elif text == "🎯 SCORE EXACT VIP":
        if not is_vip(uid):
            return await update.message.reply_text("⛔ VIP requis")
        return await update.message.reply_text("\n\n".join(score_exact_vip()))

    elif text == "📜 HISTORIQUE":
        history = get_history()
        if not history:
            return await update.message.reply_text("❌ Aucun historique")
        msg = "\n\n".join([
            f"{h['match']}\n🎯 {h['prediction']} ({h['confidence']}%)"
            for h in history
        ])
        return await update.message.reply_text(msg)

    else:
        return await update.message.reply_text("❌ Option inconnue")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("addvip", addvip))
    app.add_handler(MessageHandler(filters.TEXT, handle_buttons))

    print("🚀 BOT PRO ACTIF")
    app.run_polling()

if __name__ == "__main__":
    main()