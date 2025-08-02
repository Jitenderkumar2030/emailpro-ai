import requests
from app.core.config import get_settings
from app.models.user import User
from typing import List

settings = get_settings()

def send_push_notification(user_tokens: List[str], title: str, body: str):
    """Firebase Cloud Messaging integration"""
    # FCM push notifications
    # Campaign completion alerts
    # Reply notifications
    
    headers = {
        'Authorization': f'key={settings.FCM_SERVER_KEY}',
        'Content-Type': 'application/json'
    }
    
    payload = {
        'registration_ids': user_tokens,
        'notification': {
            'title': title,
            'body': body,
            'icon': 'ic_notification',
            'sound': 'default'
        },
        'data': data or {}
    }
    
    try:
        response = requests.post(
            'https://fcm.googleapis.com/fcm/send',
            headers=headers,
            json=payload
        )
        return response.status_code == 200
    except Exception as e:
        print(f"Push notification error: {str(e)}")
        return False

def notify_campaign_complete(user: User, campaign_name: str, stats: dict):
    """Send push notification when campaign completes"""
    if not user.fcm_token:
        return False
    
    title = "Campaign Completed"
    body = f"{campaign_name} finished with {stats.get('sent', 0)} emails sent"
    
    return send_push_notification([user.fcm_token], title, body, {
        'type': 'campaign_complete',
        'campaign_name': campaign_name,
        'stats': stats
    })

def notify_new_reply(user: User, sender_email: str):
    """Send push notification for new email reply"""
    if not user.fcm_token:
        return False
    
    title = "New Email Reply"
    body = f"You received a reply from {sender_email}"
    
    return send_push_notification([user.fcm_token], title, body, {
        'type': 'new_reply',
        'sender': sender_email
    })
