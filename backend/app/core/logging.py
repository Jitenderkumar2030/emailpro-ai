import logging
import sys
from datetime import datetime
from pathlib import Path

# Create logs directory
logs_dir = Path("logs")
logs_dir.mkdir(exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(logs_dir / f"emailproai_{datetime.now().strftime('%Y%m%d')}.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

# Create specific loggers
email_logger = logging.getLogger("email_service")
auth_logger = logging.getLogger("auth_service")
payment_logger = logging.getLogger("payment_service")
campaign_logger = logging.getLogger("campaign_service")

def log_email_sent(user_id: int, recipient: str, subject: str, success: bool):
    """Log email sending attempts"""
    status = "SUCCESS" if success else "FAILED"
    email_logger.info(f"Email {status} - User: {user_id}, To: {recipient}, Subject: {subject}")

def log_auth_attempt(email: str, success: bool, ip_address: str = None):
    """Log authentication attempts"""
    status = "SUCCESS" if success else "FAILED"
    auth_logger.info(f"Auth {status} - Email: {email}, IP: {ip_address}")

def log_payment_event(user_id: int, amount: float, status: str, order_id: str):
    """Log payment events"""
    payment_logger.info(f"Payment {status} - User: {user_id}, Amount: {amount}, Order: {order_id}")

def log_campaign_event(user_id: int, campaign_id: int, event: str, details: str = ""):
    """Log campaign events"""
    campaign_logger.info(f"Campaign {event} - User: {user_id}, Campaign: {campaign_id}, Details: {details}")