# =========================
# IMPORTS
# =========================
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
from payment import process_payment
from database import *

from games import (
    top3_games,
    vip_games,
    admin_vip_games,
    score_exact_vip
)

# =========================
# CONFIG
# =========================
load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = str(os.getenv("ADMIN_ID"))

logging.basicConfig(level=logging.INFO)

# =========================
# SECURITY
# =========================
def is_admin(uid):
    return str(uid) == ADMIN_ID

def is_vip(uid):
    return check_sub(uid) or is_vip_db(uid)

# =========================
# MENU
# =========================
keyboard = [
    ["🔥 TOP 3", "💎 VIP"],
    ["🎯 SCORE EXACT VIP", "👑 ADMIN VIP"],
    ["💳 PAYER VIP", "📊 INFOS MATCH"],
    ["🤖 AUTO PRONO", "📊 DASHBOARD"]
]

markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# =========================
# START
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 BOT BOOKMAKER PRO MAX ACTIF", reply_markup=markup)

# =========================
# ADMIN VIP ADD
# =========================
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

# =========================
# BUTTONS
# =========================
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

    elif text == "💳 PAYER VIP":
        return await update.message.reply_text("💰 Paiement Mobile Money disponible")

    elif text == "📊 INFOS MATCH":
        return await update.message.reply_text("\n\n".join(top3_games()))

    elif text == "🤖 AUTO PRONO":
        return await update.message.reply_text("🤖 IA activée")

    elif text == "📊 DASHBOARD":
        if not is_admin(uid):
            return await update.message.reply_text("⛔ refusé")
        return await update.message.reply_text("📊 Dashboard OK")

    else:
        return await update.message.reply_text("❌ Option inconnue")

# =========================
# MAIN
# =========================
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("addvip", addvip))
    app.add_handler(MessageHandler(filters.TEXT, handle_buttons))

    print("🚀 BOT BOOKMAKER PRO MAX ACTIF")
    app.run_polling()

if __name__ == "__main__":
    main()
