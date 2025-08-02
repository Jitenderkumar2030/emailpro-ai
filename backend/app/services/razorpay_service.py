# backend/app/services/razorpay_service.py
import hmac
import hashlib
import json
from app.core.config import get_settings

settings = get_settings()

RAZORPAY_SECRET = settings.RAZORPAY_SECRET

def process_webhook(body: bytes):
    data = json.loads(body.decode("utf-8"))
    # Optionally verify signature if required
    if data.get("event") == "payment.captured":
        # Update user credits or status in DB (mock logic)
        return {"message": "Payment captured", "data": data}
    return {"message": "Unhandled event", "event": data.get("event")}
