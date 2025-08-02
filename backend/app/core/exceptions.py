from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging

logger = logging.getLogger(__name__)

class EmailProAIException(Exception):
    """Base exception for EmailProAI"""
    def __init__(self, message: str, error_code: str = None):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)

class InsufficientCreditsException(EmailProAIException):
    """Raised when user has insufficient credits"""
    def __init__(self):
        super().__init__("Insufficient credits. Please upgrade your plan.", "INSUFFICIENT_CREDITS")

class PlanLimitExceededException(EmailProAIException):
    """Raised when user exceeds plan limits"""
    def __init__(self, limit_type: str):
        super().__init__(f"{limit_type} limit exceeded for your current plan.", "PLAN_LIMIT_EXCEEDED")

class EmailSendException(EmailProAIException):
    """Raised when email sending fails"""
    def __init__(self, reason: str):
        super().__init__(f"Failed to send email: {reason}", "EMAIL_SEND_FAILED")

class PaymentException(EmailProAIException):
    """Raised when payment processing fails"""
    def __init__(self, reason: str):
        super().__init__(f"Payment failed: {reason}", "PAYMENT_FAILED")

class GmailAuthException(EmailProAIException):
    """Raised when Gmail authentication fails"""
    def __init__(self, reason: str):
        super().__init__(f"Gmail authentication failed: {reason}", "GMAIL_AUTH_FAILED")

# Exception handlers
async def emailproai_exception_handler(request: Request, exc: EmailProAIException):
    logger.error(f"EmailProAI Exception: {exc.message} - Code: {exc.error_code}")
    return JSONResponse(
        status_code=400,
        content={
            "error": True,
            "message": exc.message,
            "error_code": exc.error_code,
            "timestamp": str(datetime.now())
        }
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation Error: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={
            "error": True,
            "message": "Validation failed",
            "details": exc.errors(),
            "timestamp": str(datetime.now())
        }
    )

async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    logger.error(f"HTTP Exception: {exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": exc.detail,
            "status_code": exc.status_code,
            "timestamp": str(datetime.now())
        }
    )

async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled Exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "message": "Internal server error",
            "timestamp": str(datetime.now())
        }
    )
