import requests
from app.core.config import get_settings
from app.models.user import User
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

settings = get_settings()

OUTLOOK_SCOPES = ['https://graph.microsoft.com/mail.send', 'https://graph.microsoft.com/mail.read']

def get_outlook_auth_url(user_id: str) -> str:
    """Microsoft Outlook OAuth 2.0 integration"""
    # Microsoft Graph API
    # Token management
    # Email sending via Outlook
    auth_url = (
        f"https://login.microsoftonline.com/common/oauth2/v2.0/authorize?"
        f"client_id={settings.MICROSOFT_CLIENT_ID}&"
        f"response_type=code&"
        f"redirect_uri={settings.FRONTEND_URL}/auth/outlook/callback&"
        f"scope={' '.join(OUTLOOK_SCOPES)}&"
        f"state={user_id}&"
        f"response_mode=query"
    )
    return auth_url

def exchange_outlook_code_for_tokens(code: str, state: str, db: Session) -> dict:
    token_url = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
    
    data = {
        'client_id': settings.MICROSOFT_CLIENT_ID,
        'client_secret': settings.MICROSOFT_CLIENT_SECRET,
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': f"{settings.FRONTEND_URL}/auth/outlook/callback",
        'scope': ' '.join(OUTLOOK_SCOPES)
    }
    
    response = requests.post(token_url, data=data)
    tokens = response.json()
    
    # Store tokens in database
    user_id = int(state)
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise Exception("User not found")
    
    user.outlook_access_token = tokens['access_token']
    user.outlook_refresh_token = tokens.get('refresh_token')
    user.outlook_token_expires_at = datetime.utcnow() + timedelta(seconds=tokens['expires_in'])
    user.outlook_connected = True
    
    db.commit()
    return tokens

def send_outlook_email(user: User, to_email: str, subject: str, body: str, db: Session) -> bool:
    try:
        headers = {
            'Authorization': f'Bearer {user.outlook_access_token}',
            'Content-Type': 'application/json'
        }
        
        email_data = {
            'message': {
                'subject': subject,
                'body': {
                    'contentType': 'HTML',
                    'content': body
                },
                'toRecipients': [
                    {
                        'emailAddress': {
                            'address': to_email
                        }
                    }
                ]
            }
        }
        
        response = requests.post(
            'https://graph.microsoft.com/v1.0/me/sendMail',
            headers=headers,
            json=email_data
        )
        
        return response.status_code == 202
    except Exception as e:
        print(f"Outlook send error: {str(e)}")
        return False
