# backend/app/schemas/email.py
from pydantic import BaseModel
from datetime import datetime

class EmailBase(BaseModel):
    subject: str
    body: str

class EmailCreate(EmailBase):
    pass

class EmailOut(EmailBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True