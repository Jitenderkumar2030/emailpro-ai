from typing import Dict, Any

def get_email_template(template_type: str, variables: Dict[str, Any]) -> str:
    """Get professional email template with variables"""
    
    templates = {
        "cold_outreach": """
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #2c3e50;">Hello {recipient_name},</h2>
                
                <p>I hope this email finds you well. My name is {sender_name}, and I'm reaching out from {company_name}.</p>
                
                <p>{personalized_message}</p>
                
                <div style="background-color: #f8f9fa; padding: 15px; border-left: 4px solid #007bff; margin: 20px 0;">
                    <h3 style="margin-top: 0; color: #007bff;">What we offer:</h3>
                    <ul>
                        {offer_points}
                    </ul>
                </div>
                
                <p>Would you be interested in a brief 15-minute call to discuss how we can help {company_name} achieve {goal}?</p>
                
                <p>Best regards,<br>
                {sender_name}<br>
                {sender_title}<br>
                {company_name}</p>
                
                <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee; font-size: 12px; color: #666;">
                    <img src="{tracking_pixel}" width="1" height="1" style="display: none;">
                    <p><a href="{unsubscribe_link}" style="color: #666;">Unsubscribe</a> | {company_address}</p>
                </div>
            </div>
        </body>
        </html>
        """,
        
        "follow_up": """
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #2c3e50;">Following up on our conversation</h2>
                
                <p>Hi {recipient_name},</p>
                
                <p>I wanted to follow up on my previous email about {subject}. I understand you're busy, but I believe this could be valuable for {company_name}.</p>
                
                <div style="background-color: #fff3cd; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <p style="margin: 0;"><strong>Quick reminder:</strong> {reminder_text}</p>
                </div>
                
                <p>If you're interested, I'd love to schedule a brief call at your convenience. If not, just let me know and I'll stop following up.</p>
                
                <p>Thanks for your time!</p>
                
                <p>Best,<br>
                {sender_name}</p>
                
                <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee; font-size: 12px; color: #666;">
                    <img src="{tracking_pixel}" width="1" height="1" style="display: none;">
                    <p><a href="{unsubscribe_link}" style="color: #666;">Unsubscribe</a></p>
                </div>
            </div>
        </body>
        </html>
        """,
        
        "thank_you": """
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #28a745;">Thank you, {recipient_name}!</h2>
                
                <p>I wanted to personally thank you for {reason}. It means a lot to us at {company_name}.</p>
                
                <div style="background-color: #d4edda; padding: 15px; border-radius: 5px; margin: 20px 0; border-left: 4px solid #28a745;">
                    <p style="margin: 0;">{appreciation_message}</p>
                </div>
                
                <p>If you have any questions or need assistance, please don't hesitate to reach out.</p>
                
                <p>With gratitude,<br>
                {sender_name}<br>
                {company_name}</p>
                
                <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee; font-size: 12px; color: #666;">
                    <img src="{tracking_pixel}" width="1" height="1" style="display: none;">
                </div>
            </div>
        </body>
        </html>
        """,
        
        "meeting_request": """
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #2c3e50;">Meeting Request: {meeting_subject}</h2>
                
                <p>Hi {recipient_name},</p>
                
                <p>I hope you're doing well. I'd like to schedule a meeting to discuss {meeting_purpose}.</p>
                
                <div style="background-color: #e3f2fd; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <h3 style="margin-top: 0; color: #1976d2;">Meeting Details:</h3>
                    <ul style="margin: 0;">
                        <li><strong>Duration:</strong> {duration}</li>
                        <li><strong>Proposed Date:</strong> {proposed_date}</li>
                        <li><strong>Format:</strong> {meeting_format}</li>
                    </ul>
                </div>
                
                <p><strong>Agenda:</strong></p>
                <ul>
                    {agenda_items}
                </ul>
                
                <p>Please let me know if this time works for you, or suggest an alternative that fits your schedule better.</p>
                
                <p>Looking forward to our conversation!</p>
                
                <p>Best regards,<br>
                {sender_name}<br>
                {sender_title}</p>
                
                <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee; font-size: 12px; color: #666;">
                    <img src="{tracking_pixel}" width="1" height="1" style="display: none;">
                </div>
            </div>
        </body>
        </html>
        """
    }
    
    template = templates.get(template_type, templates["cold_outreach"])
    
    # Replace variables in template
    for key, value in variables.items():
        if isinstance(value, list):
            # Handle list variables (like offer_points, agenda_items)
            value = "\n".join([f"<li>{item}</li>" for item in value])
        template = template.replace(f"{{{key}}}", str(value))
    
    return template

def add_tracking_elements(html_content: str, tracking_id: str, unsubscribe_token: str, base_url: str) -> str:
    """Add tracking pixel and unsubscribe link to email"""
    tracking_pixel = f"{base_url}/api/campaign/tracking/pixel/{tracking_id}"
    unsubscribe_link = f"{base_url}/unsubscribe/{unsubscribe_token}"
    
    html_content = html_content.replace("{tracking_pixel}", tracking_pixel)
    html_content = html_content.replace("{unsubscribe_link}", unsubscribe_link)
    
    return html_content