# backend/app/api/followup.py
from fastapi import APIRouter
from app.services.followup_service import run_followups

router = APIRouter()

@router.post("/followups/trigger")
async def trigger_followups():
    try:
        result = run_followups()
        return {"status": "triggered", "processed": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
