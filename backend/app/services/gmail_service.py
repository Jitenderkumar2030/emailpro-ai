from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from email.mime.text import MIMEText
import base64
import json
from datetime import datetime, timedelta
from app.core.config import get_settings
from app.models.user import User
from sqlalchemy.orm import Session

settings = get_settings()

SCOPES = ['https://www.googleapis.com/auth/gmail.send', 'https://www.googleapis.com/auth/gmail.readonly']

def get_gmail_auth_url(user_id: str) -> str:
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [f"{settings.FRONTEND_URL}/auth/gmail/callback"]
            }
        },
        scopes=SCOPES
    )
    flow.redirect_uri = f"{settings.FRONTEND_URL}/auth/gmail/callback"
    
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        state=user_id,
        prompt='consent'
    )
    
    return authorization_url

def exchange_code_for_tokens(code: str, state: str, db: Session) -> dict:
    """Exchange authorization code for access tokens and store in database"""
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [f"{settings.FRONTEND_URL}/auth/gmail/callback"]
            }
        },
        scopes=SCOPES
    )
    flow.redirect_uri = f"{settings.FRONTEND_URL}/auth/gmail/callback"
    
    # Exchange code for tokens
    flow.fetch_token(code=code)
    credentials = flow.credentials
    
    # Store tokens in database
    user_id = int(state)  # state contains user_id
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise Exception("User not found")
    
    user.gmail_access_token = credentials.token
    user.gmail_refresh_token = credentials.refresh_token
    user.gmail_token_expires_at = credentials.expiry
    user.gmail_connected = True
    
    db.commit()
    
    return {
        "access_token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "expires_at": credentials.expiry.isoformat() if credentials.expiry else None
    }

def refresh_gmail_token(user: User, db: Session) -> Credentials:
    """Refresh expired Gmail tokens"""
    credentials = Credentials(
        token=user.gmail_access_token,
        refresh_token=user.gmail_refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=settings.GOOGLE_CLIENT_ID,
        client_secret=settings.GOOGLE_CLIENT_SECRET,
        scopes=SCOPES
    )
    
    if credentials.expired:
        credentials.refresh(Request())
        
        # Update database with new tokens
        user.gmail_access_token = credentials.token
        user.gmail_token_expires_at = credentials.expiry
        db.commit()
    
    return credentials

def send_gmail(user: User, to_email: str, subject: str, body: str) -> bool:
    """Send emails via Gmail API with OAuth 2.0"""
    # Full OAuth 2.0 implementation
    # Token refresh automation
    # HTML email support
    try:
        credentials = refresh_gmail_token(user, db)
        service = build('gmail', 'v1', credentials=credentials)
        
        message = MIMEText(body, 'html')
        message['to'] = to_email
        message['subject'] = subject
        message['from'] = user.email
        
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        
        result = service.users().messages().send(
            userId='me',
            body={'raw': raw_message}
        ).execute()
        
        return True
    except Exception as e:
        print(f"Gmail send error: {str(e)}")
        return False

def check_gmail_replies(user: User, db: Session) -> list:
    """Check for new replies in Gmail"""
    try:
        credentials = refresh_gmail_token(user, db)
        service = build('gmail', 'v1', credentials=credentials)
        
        # Get messages from last 24 hours
        import time
        yesterday = int(time.time()) - 86400
        
        results = service.users().messages().list(
            userId='me',
            q=f'is:unread after:{yesterday}'
        ).execute()
        
        messages = results.get('messages', [])
        replies = []
        
        for msg in messages:
            message = service.users().messages().get(userId='me', id=msg['id']).execute()
            headers = message['payload'].get('headers', [])
            
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '')
            sender = next((h['value'] for h in headers if h['name'] == 'From'), '')
            
            if 'Re:' in subject or 'RE:' in subject:
                replies.append({
                    'id': msg['id'],
                    'subject': subject,
                    'sender': sender,
                    'snippet': message.get('snippet', '')
                })
        
        return replies
    except Exception as e:
        print(f"Gmail reply check error: {str(e)}")
        return []
