# backend/app/api/history.py
from fastapi import APIRouter
from app.services.history_service import fetch_history

router = APIRouter()

@router.get("/history")
async def get_email_history():
    try:
        history = fetch_history()
        return {"emails": history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
