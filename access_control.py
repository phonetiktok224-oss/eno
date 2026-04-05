from config import ADMIN_IDS, VIP_USERS

def is_admin(user_id):
    return user_id in ADMIN_IDS

def is_vip(user_id):
    return user_id in VIP_USERS or is_admin(user_id)

def require_vip(user_id):
    if is_admin(user_id):
        return True
    return user_id in VIP_USERS