def process_payment(method, phone, amount):
    if method in ["MTN", "ORANGE"]:
        return {"status": "success"}
    return {"status": "failed"}