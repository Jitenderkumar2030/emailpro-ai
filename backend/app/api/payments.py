from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.cashfree_service import create_payment_order, process_payment_webhook, get_payment_status
from app.models.user import PlanType
from pydantic import BaseModel

router = APIRouter()

class PaymentOrderRequest(BaseModel):
    user_id: int
    plan_type: str

@router.post("/create-order")
async def create_payment_order_endpoint(payload: PaymentOrderRequest, db: Session = Depends(get_db)):
    try:
        plan_type = PlanType(payload.plan_type.lower())
        order = create_payment_order(payload.user_id, plan_type, db)
        return {"status": "success", "order": order}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/cashfree/webhook")
async def cashfree_webhook(request: Request, db: Session = Depends(get_db)):
    try:
        body = await request.json()
        result = process_payment_webhook(body, db)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/status/{order_id}")
async def payment_status(order_id: str):
    try:
        status = get_payment_status(order_id)
        return {"status": "success", "payment": status}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
