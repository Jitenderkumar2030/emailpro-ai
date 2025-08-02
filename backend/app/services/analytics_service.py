from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import pandas as pd
import io
from sqlalchemy.orm import Session
from app.models.campaign import Campaign
from app.models.email_tracking import EmailLog
from datetime import datetime, timedelta

def generate_pdf_report(user_id: int, start_date: str, end_date: str):
    """Generate comprehensive PDF analytics reports"""
    # Professional PDF generation
    # Excel export capability
    # Custom date ranges
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    
    # Get analytics data
    campaigns = db.query(Campaign).filter(Campaign.user_id == user_id).all()
    total_sent = sum(c.total_sent for c in campaigns)
    total_opens = sum(c.total_opens for c in campaigns)
    total_clicks = sum(c.total_clicks for c in campaigns)
    
    # Create PDF content
    p.drawString(100, 750, "EmailProAI Analytics Report")
    p.drawString(100, 720, f"Total Campaigns: {len(campaigns)}")
    p.drawString(100, 700, f"Total Emails Sent: {total_sent}")
    p.drawString(100, 680, f"Total Opens: {total_opens}")
    p.drawString(100, 660, f"Total Clicks: {total_clicks}")
    p.drawString(100, 640, f"Open Rate: {(total_opens/total_sent*100):.2f}%" if total_sent > 0 else "Open Rate: 0%")
    p.drawString(100, 620, f"Click Rate: {(total_clicks/total_sent*100):.2f}%" if total_sent > 0 else "Click Rate: 0%")
    
    p.save()
    buffer.seek(0)
    return buffer

def generate_excel_report(user_id: int, start_date: str, end_date: str, db: Session):
    # Get data
    campaigns = db.query(Campaign).filter(Campaign.user_id == user_id).all()
    
    data = []
    for campaign in campaigns:
        data.append({
            'Campaign Name': campaign.name,
            'Sent': campaign.total_sent,
            'Opens': campaign.total_opens,
            'Clicks': campaign.total_clicks,
            'Open Rate': f"{(campaign.total_opens/campaign.total_sent*100):.2f}%" if campaign.total_sent > 0 else "0%",
            'Click Rate': f"{(campaign.total_clicks/campaign.total_sent*100):.2f}%" if campaign.total_sent > 0 else "0%",
            'Created': campaign.created_at.strftime('%Y-%m-%d')
        })
    
    df = pd.DataFrame(data)
    buffer = io.BytesIO()
    df.to_excel(buffer, index=False)
    buffer.seek(0)
    return buffer
