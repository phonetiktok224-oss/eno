# =========================
# IMPORTS
# =========================
import os
import random
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

from data_sources import get_all_matches
from ai_engine import analyse_match
from subscription import check_sub
from payment import process_payment
from database import *

# ✅ MODULE JEUX
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
ADMIN_ID = os.getenv("ADMIN_ID")

if not TOKEN:
    raise ValueError("❌ BOT_TOKEN manquant")

if not ADMIN_ID:
    raise ValueError("❌ ADMIN_ID manquant")

logging.basicConfig(level=logging.INFO)

ADMIN_VIP_USERS = set()

# =========================
# 🔐 SECURITY
# =========================
def is_admin(uid: str):
    return str(uid) == str(ADMIN_ID)

def is_vip_access(uid: str):
    uid = str(uid)

    if is_admin(uid):
        return True

    if uid in ADMIN_VIP_USERS or is_admin_vip_db(uid):
        return True

    if check_sub(uid) or is_vip_db(uid):
        return True

    return False

# =========================
# MENU
# =========================
keyboard = [
    ["🔥 TOP 3", "💎 VIP"],
    ["🎯 SCORE EXACT VIP", "👑 ADMIN VIP"],
]

markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# =========================
# START
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 Bienvenue sur le BOT PRONOS PRO\n📊 Matchs du jour + Stats avancées",
        reply_markup=markup
    )

# =========================
# BUTTONS
# =========================
async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    uid = str(update.effective_user.id)

    if text == "🔥 TOP 3":
        data = top3_games()
        await update.message.reply_text("\n\n".join(data))
        return

    if text == "💎 VIP":
        if not is_vip_access(uid):
            await update.message.reply_text("⛔ VIP requis")
            return

        data = vip_games()
        await update.message.reply_text("\n\n".join(data))
        return

    if text == "👑 ADMIN VIP":
        if not is_admin(uid):
            await update.message.reply_text("⛔ ADMIN VIP seulement")
            return

        data = admin_vip_games()
        await update.message.reply_text("\n\n".join(data))
        return

    if text == "🎯 SCORE EXACT VIP":
        if not is_vip_access(uid):
            await update.message.reply_text("⛔ VIP requis")
            return

        data = score_exact_vip()
        await update.message.reply_text("\n\n".join(data))
        return

    # ✅ sécurité ajoutée
    await update.message.reply_text("❌ Option inconnue")

# =========================
# MAIN
# =========================
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_buttons))

    print("🚀 BOT ACTIF FINAL PRO")
    app.run_polling()

if __name__ == "__main__":
    main()
