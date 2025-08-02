# backend/app/schemas/campaign.py
from pydantic import BaseModel
from datetime import datetime

class CampaignBase(BaseModel):
    name: str

class CampaignCreate(CampaignBase):
    pass

class CampaignOut(CampaignBase):
    id: int
    created_at: datetime
    sent: bool

    class Config:
        orm_mode = True
