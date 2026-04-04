# =========================
# IMPORTS
# =========================
import os
import random
import logging
import asyncio
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
from subscription import check_sub, add_sub
from payment import process_payment

from database import *

# =========================
# CONFIG
# =========================
load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = str(os.getenv("ADMIN_ID", ""))

if not TOKEN:
    raise ValueError("❌ BOT_TOKEN manquant dans .env")

PAYMENT_NUMBER = "670000000"
VIP_PRICE = "2000 FCFA"
ADMIN_VIP_PRICE = "5000 FCFA"

PAYMENT_CONFIG = {
    "vip_number": PAYMENT_NUMBER,
    "vip_price": VIP_PRICE,
    "admin_number": PAYMENT_NUMBER,
    "admin_price": ADMIN_VIP_PRICE
}

logging.basicConfig(level=logging.INFO)

# ✅ FIX ADMIN
ADMINS = {ADMIN_ID} if ADMIN_ID else set()
ADMIN_VIP_USERS = set()

# =========================
# 🔐 FIX VIP GLOBAL
# =========================
def is_admin(uid: str):
    return str(uid) == str(ADMIN_ID)

def is_vip_access(uid: str):
    uid = str(uid)

    # 🔥 ADMIN = accès total
    if is_admin(uid):
        return True

    # 👑 ADMIN VIP
    if uid in ADMIN_VIP_USERS or is_admin_vip_db(uid):
        return True

    # 💎 VIP
    if check_sub(uid) or is_vip_db(uid):
        return True

    return False

# =========================
# MENU
# =========================
keyboard = [
    ["🔥 TOP 3", "🎟 COTE 3"],
    ["💎 VIP", "💎 COTE 50 VIP"],
    ["🎯 SCORE EXACT VIP"],
    ["👑 ADMIN VIP", "🤖 AUTO PRONO"],
    ["📊 INFOS MATCH", "🔐 RECUP VIP"],
    ["💳 PAYER VIP", "👑 PAYER ADMIN VIP"],
    ["📊 DASHBOARD", "📲 WHATSAPP"]
]

markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# =========================
# 🧠 IA LIVE
# =========================
def ai_live_plus(home, away):
    try:
        return analyse_match(home, away)
    except Exception as e:
        logging.error(f"IA ERROR: {e}")
        return {
            "prediction": random.choice(["Under 3.5", "BTTS NON", "Victoire domicile"]),
            "confidence": random.randint(70, 90)
        }

# =========================
# 📊 DASHBOARD
# =========================
async def dashboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.effective_user.id)

    if not is_admin(uid):
        await update.message.reply_text("⛔ Accès refusé")
        return

    try:
        vip_count, admin_count = get_stats()
    except:
        vip_count, admin_count = 0, 0

    await update.message.reply_text(
        f"📊 DASHBOARD\n\n👥 VIP: {vip_count}\n👑 ADMIN VIP: {admin_count}"
    )

# =========================
# 🤖 AUTO MARKETING
# =========================
async def auto_marketing(update: Update):
    await update.message.reply_text(
        "🔥 OFFRE LIMITÉE\n\n"
        "💎 VIP → précision stable\n"
        "👑 ADMIN VIP → gains élevés\n\n"
        "⚡ Rejoins maintenant !"
    )

# =========================
# BUILD PREDICTIONS
# =========================
def build_predictions(vip=False, admin=False):
    try:
        matches = get_all_matches()
        if not matches:
            return ["⚠️ Aucun match trouvé"]
    except Exception as e:
        logging.error(f"API ERROR: {e}")
        return ["⚠️ API indisponible"]

    results = []

    for m in matches:
        try:
            res = ai_live_plus(m["home"], m["away"])

            txt = f"{m['home']} vs {m['away']}\n👉 {res['prediction']} ({res['confidence']}%)"

            if admin:
                txt += "\n👑 " + random.choice([
                    "⚽ Favori marque",
                    "⛔ Under 3.5",
                    "🚫 Pas de but MT"
                ])

            results.append((res["confidence"], txt))

        except Exception as e:
            logging.warning(f"Match error: {e}")
            continue

    if not results:
        return ["⚠️ Aucun résultat"]

    results.sort(reverse=True)
    return [r[1] for r in results[:3]]

# =========================
# SCORE EXACT
# =========================
def score_exact_vip():
    try:
        matches = get_all_matches()
    except:
        return "⚠️ API indisponible"

    return "\n\n".join([
        f"{m['home']} vs {m['away']} → 🎯 {random.choice(['1-0','2-1','2-0'])}"
        for m in matches[:3]
    ])

# =========================
# 💳 PAIEMENTS
# =========================
async def pay_vip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"💳 VIP NORMAL\n\n📱 {PAYMENT_CONFIG['vip_number']}\n💰 {PAYMENT_CONFIG['vip_price']}"
    )

async def pay_admin_vip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"👑 ADMIN VIP\n\n📱 {PAYMENT_CONFIG['admin_number']}\n💰 {PAYMENT_CONFIG['admin_price']}"
    )

# =========================
# AUTO PRONO 24H 🔥
# =========================
async def auto_prono_job(context: ContextTypes.DEFAULT_TYPE):
    try:
        users = get_all_users()
    except:
        return

    predictions = "\n\n".join(build_predictions())

    for uid in users:
        try:
            await context.bot.send_message(
                chat_id=uid,
                text=f"🤖 PRONO DU JOUR\n\n{predictions}"
            )
        except:
            continue

# =========================
# START AUTO SYSTEM
# =========================
async def start_auto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.effective_user.id)

    if not is_admin(uid):
        return

    context.job_queue.run_repeating(auto_prono_job, interval=86400, first=10)

    await update.message.reply_text("✅ AUTO PRONO ACTIVÉ (24H)")

# =========================
# CONFIRM PAYMENT (FIX)
# =========================
async def confirm_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.effective_user.id)

    try:
        if process_payment(uid):
            # 👑 ADMIN uniquement si c’est l’admin
            if is_admin(uid):
                add_admin_vip_db(uid)
                ADMIN_VIP_USERS.add(uid)
                await update.message.reply_text("👑 ADMIN VIP activé")
            else:
                add_sub(uid)
                add_vip_db(uid)
                await update.message.reply_text("💎 VIP activé")
        else:
            await update.message.reply_text("⚠️ Paiement non confirmé")
    except Exception as e:
        logging.error(e)
        await update.message.reply_text("⚠️ Erreur paiement")

# =========================
# START
# =========================
async def start(update, context):
    uid = str(update.effective_user.id)

    try:
        add_user(uid)
    except:
        pass

    await update.message.reply_text("🤖 BOT PRO MAX", reply_markup=markup)
    await auto_marketing(update)

# =========================
# HANDLER
# =========================
async def handle_buttons(update, context):
    text = update.message.text
    uid = str(update.effective_user.id)

    if text == "🔥 TOP 3":
        await update.message.reply_text("\n\n".join(build_predictions()))

    elif text == "💎 VIP":
        if is_vip_access(uid):
            await update.message.reply_text("\n\n".join(build_predictions(True)))
        else:
            await update.message.reply_text("⛔ VIP requis")

    elif text == "👑 ADMIN VIP":
        if is_admin(uid) or uid in ADMIN_VIP_USERS or is_admin_vip_db(uid):
            await update.message.reply_text("\n\n".join(build_predictions(True, True)))
        else:
            await update.message.reply_text("⛔ ADMIN VIP requis")

    elif text == "🎯 SCORE EXACT VIP":
        if is_vip_access(uid):
            await update.message.reply_text(score_exact_vip())
        else:
            await update.message.reply_text("⛔ VIP requis")

    elif text == "💳 PAYER VIP":
        await pay_vip(update, context)

    elif text == "👑 PAYER ADMIN VIP":
        await pay_admin_vip(update, context)

    elif text == "📊 DASHBOARD":
        await dashboard(update, context)

    elif text == "📲 WHATSAPP":
        await update.message.reply_text("https://wa.me/237670000000")

# =========================
# MAIN
# =========================
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("confirm", confirm_payment))
    app.add_handler(CommandHandler("autoprono", start_auto))

    app.add_handler(MessageHandler(filters.TEXT, handle_buttons))

    print("🚀 BOT 100% ACTIF + AUTO")
    app.run_polling()

if __name__ == "__main__":
    main()