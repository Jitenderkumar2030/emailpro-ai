import requests
import hmac
import hashlib
import json
from datetime import datetime
from app.core.config import get_settings
from app.models.user import User, PlanType
from sqlalchemy.orm import Session

settings = get_settings()

CASHFREE_BASE_URL = "https://sandbox.cashfree.com/pg"  # Use production URL for live
CASHFREE_APP_ID = settings.CASHFREE_APP_ID
CASHFREE_SECRET_KEY = settings.CASHFREE_SECRET_KEY

PLAN_PRICES = {
    PlanType.STARTER: {"amount": 999, "name": "Starter Plan"},
    PlanType.PRO: {"amount": 2999, "name": "Pro Plan"},
    PlanType.LIFETIME: {"amount": 9999, "name": "Lifetime Plan"}
}

def create_payment_order(user_id: int, plan_type: PlanType, db: Session) -> dict:
    """Create a payment order with Cashfree"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise Exception("User not found")
    
    plan_info = PLAN_PRICES.get(plan_type)
    if not plan_info:
        raise Exception("Invalid plan type")
    
    order_id = f"ORDER_{user_id}_{int(datetime.now().timestamp())}"
    
    payload = {
        "order_id": order_id,
        "order_amount": plan_info["amount"],
        "order_currency": "INR",
        "customer_details": {
            "customer_id": str(user_id),
            "customer_name": user.full_name or user.email,
            "customer_email": user.email,
            "customer_phone": "9999999999"  # You might want to add phone to user model
        },
        "order_meta": {
            "return_url": f"{settings.FRONTEND_URL}/payment/success",
            "notify_url": f"{settings.BACKEND_URL}/api/payments/cashfree/webhook",
            "payment_methods": "cc,dc,nb,upi,wallet"
        },
        "order_note": f"Payment for {plan_info['name']}"
    }
    
    headers = {
        "Content-Type": "application/json",
        "x-api-version": "2022-09-01",
        "x-client-id": CASHFREE_APP_ID,
        "x-client-secret": CASHFREE_SECRET_KEY
    }
    
    response = requests.post(
        f"{CASHFREE_BASE_URL}/orders",
        headers=headers,
        json=payload
    )
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Payment order creation failed: {response.text}")

def verify_payment_signature(order_id: str, order_amount: str, signature: str) -> bool:
    """Verify Cashfree payment signature"""
    payload = f"{order_id}{order_amount}"
    expected_signature = hmac.new(
        CASHFREE_SECRET_KEY.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(expected_signature, signature)

def process_payment_webhook(payload: dict, db: Session) -> dict:
    """Process Cashfree payment webhook"""
    try:
        order_id = payload.get("order_id")
        payment_status = payload.get("payment_status")
        order_amount = payload.get("order_amount")
        signature = payload.get("signature")
        
        # Verify signature
        if not verify_payment_signature(order_id, str(order_amount), signature):
            raise Exception("Invalid signature")
        
        if payment_status == "SUCCESS":
            # Extract user_id from order_id
            user_id = int(order_id.split("_")[1])
            user = db.query(User).filter(User.id == user_id).first()
            
            if not user:
                raise Exception("User not found")
            
            # Determine plan type based on amount
            plan_type = None
            for plan, info in PLAN_PRICES.items():
                if info["amount"] == int(order_amount):
                    plan_type = plan
                    break
            
            if not plan_type:
                raise Exception("Invalid payment amount")
            
            # Update user plan
            user.plan_type = plan_type
            if plan_type == PlanType.LIFETIME:
                user.plan_expires_at = None  # Lifetime plan never expires
            else:
                from datetime import timedelta
                user.plan_expires_at = datetime.utcnow() + timedelta(days=30)
            
            # Reset usage counters
            user.emails_generated_today = 0
            user.credits = 1000 if plan_type != PlanType.FREE else 3
            
            db.commit()
            
            return {"status": "success", "message": "Payment processed successfully"}
        
        return {"status": "failed", "message": "Payment failed"}
        
    except Exception as e:
        return {"status": "error", "message": str(e)}

def get_payment_status(order_id: str) -> dict:
    """Get payment status from Cashfree"""
    headers = {
        "x-api-version": "2022-09-01",
        "x-client-id": CASHFREE_APP_ID,
        "x-client-secret": CASHFREE_SECRET_KEY
    }
    
    response = requests.get(
        f"{CASHFREE_BASE_URL}/orders/{order_id}",
        headers=headers
    )
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to get payment status: {response.text}")
