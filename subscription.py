# subscription.py

subscribers = set()

def check_sub(user_id):
    return user_id in subscribers

def add_sub(user_id):
    subscribers.add(user_id)

def remove_sub(user_id):
    subscribers.discard(user_id)