# backend/app/services/campaign_service.py
import csv
import io
from typing import List, Dict
from app.services.smtp_service import send_email
from app.utils.email_merge_tags import merge_tags
from app.services.openai_service import generate_email

async def process_campaign_csv(file) -> List[Dict[str, str]]:
    contents = await file.read()
    decoded = contents.decode("utf-8")
    reader = csv.DictReader(io.StringIO(decoded))
    sent_emails = []

    for row in reader:
        context = merge_tags("We're offering a special deal to [company]", row)
        email_body = generate_email("Product offer", "Friendly", context)
        send_email(to_email=row['email'], subject="Exciting Offer from EmailProAI", body=email_body)
        sent_emails.append({"email": row['email'], "status": "sent"})

    return sent_emails
