# backend/app/services/followup_service.py
from sqlalchemy.orm import Session
from app.models.followup import FollowUp
from app.models.user import User
from app.services.smtp_service import send_email
from app.db.session import get_db
from datetime import datetime

# Optional: pass db as parameter for better testability
def run_followups():
    print("🔁 Running follow-up scheduler...")
    db = next(get_db())

    # Fetch all unsent follow-ups
    unsent_followups = db.query(FollowUp).filter_by(followup_sent=False).all()

    processed = 0
    for followup in unsent_followups:
        try:
            subject = "Just checking in – any thoughts?"
            body = f"Hi there,\n\nJust following up on our previous conversation. Let me know if you have any questions.\n\nBest,\nEmailProAI Team"
            send_email(to_email=followup.contact_email, subject=subject, body=body)

            followup.followup_sent = True
            followup.sent_at = datetime.utcnow()
            db.commit()
            processed += 1
        except Exception as e:
            print(f"⚠️ Error sending follow-up to {followup.contact_email}: {str(e)}")

    print(f"✅ Follow-up processing complete. Total sent: {processed}")
    return {"total_sent": processed}

def schedule_followup(email_log_id: int, delay_hours: int = 24):
    """AI-powered follow-up automation"""
    # APScheduler integration
    # Smart follow-up logic
    # Customizable delays
