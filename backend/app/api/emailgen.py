# backend/app/api/emailgen.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from app.services.openai_service import generate_email, generate_reply, generate_subject_line

router = APIRouter()

class ReplyRequest(BaseModel):
    email: str = Field(..., example="Original email content to reply to")
    tone: str = Field(default="Professional", example="Professional")

class EmailRequest(BaseModel):
    purpose: str = Field(..., example="Cold email to potential client")
    tone: str = Field(..., example="Formal")
    context: str = Field(..., example="We're offering a 20% discount on our service.")
    include_subject: bool = Field(default=True, example=True)

@router.post("/generate")
async def generate_ai_email(payload: EmailRequest):
    try:
        email = generate_email(purpose=payload.purpose, tone=payload.tone, context=payload.context)
        
        response_data = {"email": email}
        
        if payload.include_subject:
            subject = generate_subject_line(payload.purpose, payload.context, payload.tone)
            response_data["subject"] = subject
            
        return response_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/reply")
async def generate_ai_reply(payload: ReplyRequest):
    try:
        reply = generate_reply(original_email=payload.email, tone=payload.tone)
        return {"reply": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
