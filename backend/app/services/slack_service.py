import requests
from app.core.config import get_settings

settings = get_settings()

def send_slack_notification(webhook_url: str, message: str, campaign_name: str = None):
    """Send Slack notification for campaign completion"""
    
    if campaign_name:
        slack_message = {
            "text": f"📧 Campaign Update: {campaign_name}",
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*Campaign:* {campaign_name}\n*Status:* {message}"
                    }
                }
            ]
        }
    else:
        slack_message = {"text": message}
    
    try:
        response = requests.post(webhook_url, json=slack_message)
        return response.status_code == 200
    except Exception as e:
        print(f"Slack notification error: {str(e)}")
        return False

def notify_campaign_completion(webhook_url: str, campaign_name: str, stats: dict):
    """Send detailed campaign completion notification"""
    message = (
        f"✅ *Campaign Completed: {campaign_name}*\n\n"
        f"📊 *Results:*\n"
        f"• Emails Sent: {stats.get('sent', 0)}\n"
        f"• Opens: {stats.get('opens', 0)} ({stats.get('open_rate', 0):.1f}%)\n"
        f"• Clicks: {stats.get('clicks', 0)} ({stats.get('click_rate', 0):.1f}%)\n"
        f"• Replies: {stats.get('replies', 0)}"
    )
    
    return send_slack_notification(webhook_url, message, campaign_name)