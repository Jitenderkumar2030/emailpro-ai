import imaplib
import email
from email.header import decode_header
from datetime import datetime, timedelta
from typing import List, Dict
from app.core.config import get_settings
from app.models.user import User
from app.services.gmail_service import check_gmail_replies
from sqlalchemy.orm import Session

settings = get_settings()

def check_imap_replies(user_email: str, password: str, since_hours: int = 24) -> List[Dict]:
    """Check for replies using IMAP"""
    replies = []
    
    try:
        # Connect to IMAP server (Gmail example)
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(user_email, password)
        mail.select("inbox")
        
        # Search for emails from the last 24 hours
        since_date = (datetime.now() - timedelta(hours=since_hours)).strftime("%d-%b-%Y")
        
        # Search for unread emails with "Re:" in subject
        status, messages = mail.search(None, f'(UNSEEN SINCE {since_date} SUBJECT "Re:")')
        
        if status == "OK":
            for msg_id in messages[0].split():
                status, msg_data = mail.fetch(msg_id, "(RFC822)")
                
                if status == "OK":
                    email_body = msg_data[0][1]
                    email_message = email.message_from_bytes(email_body)
                    
                    # Decode subject
                    subject = decode_header(email_message["Subject"])[0][0]
                    if isinstance(subject, bytes):
                        subject = subject.decode()
                    
                    # Get sender
                    sender = email_message["From"]
                    
                    # Get message content
                    content = ""
                    if email_message.is_multipart():
                        for part in email_message.walk():
                            if part.get_content_type() == "text/plain":
                                content = part.get_payload(decode=True).decode()
                                break
                    else:
                        content = email_message.get_payload(decode=True).decode()
                    
                    replies.append({
                        "subject": subject,
                        "sender": sender,
                        "content": content[:500],  # First 500 chars
                        "received_at": datetime.now().isoformat()
                    })
        
        mail.close()
        mail.logout()
        
    except Exception as e:
        print(f"IMAP reply check error: {str(e)}")
    
    return replies

def check_user_replies(user: User, db: Session) -> List[Dict]:
    """Check for replies for a specific user"""
    replies = []
    
    # If user has Gmail connected, use Gmail API
    if user.gmail_connected and user.gmail_access_token:
        try:
            gmail_replies = check_gmail_replies(user, db)
            replies.extend(gmail_replies)
        except Exception as e:
            print(f"Gmail reply check failed for user {user.id}: {str(e)}")
    
    # Fallback to IMAP if SMTP credentials are available
    if settings.SMTP_USER and settings.SMTP_PASS:
        try:
            imap_replies = check_imap_replies(settings.SMTP_USER, settings.SMTP_PASS)
            replies.extend(imap_replies)
        except Exception as e:
            print(f"IMAP reply check failed: {str(e)}")
    
    return replies

def process_reply_detection(db: Session) -> Dict:
    """Process reply detection for all users"""
    from app.models.email_tracking import EmailLog
    
    processed = 0
    detected_replies = 0
    
    try:
        # Get all users with email tracking enabled
        users = db.query(User).filter(User.is_active == True).all()
        
        for user in users:
            try:
                replies = check_user_replies(user, db)
                
                for reply in replies:
                    # Try to match reply to sent emails
                    # This is a simplified matching - you might want more sophisticated logic
                    subject_without_re = reply["subject"].replace("Re: ", "").replace("RE: ", "")
                    
                    # Find matching sent email
                    sent_email = db.query(EmailLog).filter(
                        EmailLog.user_id == user.id,
                        EmailLog.subject.contains(subject_without_re),
                        EmailLog.is_replied == False
                    ).first()
                    
                    if sent_email:
                        sent_email.is_replied = True
                        sent_email.replied_at = datetime.now()
                        detected_replies += 1
                
                processed += 1
                
            except Exception as e:
                print(f"Error processing replies for user {user.id}: {str(e)}")
        
        db.commit()
        
        return {
            "status": "success",
            "users_processed": processed,
            "replies_detected": detected_replies
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

# Scheduled function to run reply detection
def scheduled_reply_check():
    """Scheduled function to check for replies"""
    from app.db.session import get_db
    
    db = next(get_db())
    try:
        result = process_reply_detection(db)
        print(f"Reply detection completed: {result}")
    finally:
        db.close()
