# =========================
# 💾 DATABASE SIMPLE
# =========================
import json
import os

DB_FILE = "db.json"

def load_db():
    if not os.path.exists(DB_FILE):
        return {"vip": [], "history": []}

    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except:
        return {"vip": [], "history": []}

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)

# =========================
# VIP
# =========================
def is_vip_db(uid):
    db = load_db()
    return uid in db["vip"]

def add_vip_db(uid):
    db = load_db()
    if uid not in db["vip"]:
        db["vip"].append(uid)
        save_db(db)

# =========================
# HISTORIQUE
# =========================
def save_prono(data):
    db = load_db()
    db["history"].append(data)
    save_db(db)

def get_history():
    db = load_db()
    return db["history"][-20:]