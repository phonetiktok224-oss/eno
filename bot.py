# =========================
# 🤖 TELEGRAM BOT PRO MAX (SYNC FINAL)
# =========================

# =========================
# 🔐 CONFIG TOKEN (.env)
# =========================
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

# Vérification token
if not TOKEN:
    raise ValueError("❌ BOT_TOKEN manquant dans le fichier .env")

# =========================
# IMPORT TELEGRAM
# =========================
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# =========================
# 🔐 CONFIG ADMIN
# =========================
ADMIN_IDS = [123456789]  # 👉 remplace par TON ID
VIP_USERS = set()

# =========================
# IMPORT GAMES
# =========================
from games import top3_games, vip_games, admin_vip_games, score_exact_vip

# =========================
# 🛡 SAFE EXECUTION
# =========================
def safe_call(func):
    try:
        data = func()
        return data if data else ["⚠️ Aucun match disponible"]
    except Exception as e:
        print("Erreur:", e)
        return ["❌ Erreur récupération des matchs"]

# =========================
# 🎮 START
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 BOT PRONOS PRO MAX\n\n"
        "🆓 /free → Matchs gratuits\n"
        "💎 /vip → Analyse VIP\n"
        "👑 /admin → Mode Pro\n"
    )

# =========================
# 🆓 FREE
# =========================
async def free(update: Update, context: ContextTypes.DEFAULT_TYPE):
    games = safe_call(top3_games)
    await update.message.reply_text("\n\n".join(games))

# =========================
# 💎 VIP
# =========================
async def vip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id in ADMIN_IDS or user_id in VIP_USERS:
        games = safe_call(vip_games)
        await update.message.reply_text("\n\n".join(games))
    else:
        await update.message.reply_text("❌ Accès VIP requis")

# =========================
# 👑 ADMIN
# =========================
async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id in ADMIN_IDS:
        games = safe_call(admin_vip_games)
        await update.message.reply_text("\n\n".join(games))
    else:
        await update.message.reply_text("❌ Accès ADMIN uniquement")

# =========================
# 🎯 SCORE EXACT (ADMIN)
# =========================
async def score(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id in ADMIN_IDS:
        games = safe_call(score_exact_vip)
        await update.message.reply_text("\n\n".join(games))
    else:
        await update.message.reply_text("❌ Réservé ADMIN")

# =========================
# ➕ AJOUT VIP
# =========================
async def add_vip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id in ADMIN_IDS:
        if not context.args:
            await update.message.reply_text("❌ Usage: /addvip ID")
            return

        try:
            target = int(context.args[0])
            VIP_USERS.add(target)
            await update.message.reply_text(f"✅ {target} ajouté VIP")
        except:
            await update.message.reply_text("❌ ID invalide")
    else:
        await update.message.reply_text("❌ Accès refusé")

# =========================
# ➖ SUPPRIMER VIP
# =========================
async def remove_vip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id in ADMIN_IDS:
        if not context.args:
            await update.message.reply_text("❌ Usage: /removevip ID")
            return

        try:
            target = int(context.args[0])
            VIP_USERS.discard(target)
            await update.message.reply_text(f"❌ {target} retiré VIP")
        except:
            await update.message.reply_text("❌ ID invalide")
    else:
        await update.message.reply_text("❌ Accès refusé")

# =========================
# 📋 LISTE VIP
# =========================
async def list_vip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id in ADMIN_IDS:
        if VIP_USERS:
            await update.message.reply_text(
                "💎 LISTE VIP:\n" + "\n".join(map(str, VIP_USERS))
            )
        else:
            await update.message.reply_text("Aucun VIP enregistré")
    else:
        await update.message.reply_text("❌ Accès refusé")

# =========================
# 📖 HELP ADMIN
# =========================
async def help_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id in ADMIN_IDS:
        await update.message.reply_text(
            "📖 GUIDE ADMIN PRO MAX\n\n"
            "🎮 COMMANDES:\n"
            "/start → démarrer le bot\n"
            "/free → matchs gratuits\n"
            "/vip → analyse VIP\n"
            "/admin → stratégie complète\n"
            "/score → score exact\n\n"
            "⚙️ VIP:\n"
            "/addvip ID\n"
            "/removevip ID\n"
            "/listvip\n\n"
            "🧠 STRUCTURE:\n"
            "FREE → Top 3\n"
            "VIP → Analyse avancée\n"
            "ADMIN → stratégie + score exact\n\n"
            "🚀 CONSEIL:\n"
            "Toujours valider avec ADMIN"
        )
    else:
        await update.message.reply_text("❌ Réservé ADMIN")

# =========================
# 🚀 MAIN
# =========================
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("free", free))
    app.add_handler(CommandHandler("vip", vip))
    app.add_handler(CommandHandler("admin", admin))
    app.add_handler(CommandHandler("score", score))

    app.add_handler(CommandHandler("addvip", add_vip))
    app.add_handler(CommandHandler("removevip", remove_vip))
    app.add_handler(CommandHandler("listvip", list_vip))

    app.add_handler(CommandHandler("help", help_admin))

    print("✅ BOT PRO MAX LANCÉ")
    app.run_polling()

# =========================
# ▶️ RUN
# =========================
if __name__ == "__main__":
    main()
