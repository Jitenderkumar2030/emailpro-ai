# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.scheduler import start_scheduler
from app.core.exceptions import (
    EmailProAIException, 
    emailproai_exception_handler,
    validation_exception_handler,
    http_exception_handler,
    general_exception_handler
)
from app.core.logging import email_logger
from app.api import auth, emailgen, campaign, followup, history, payments, users, teams, analytics, scheduling, mobile

app = FastAPI(title="EmailProAI API", version="1.0.0")

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handlers
app.add_exception_handler(EmailProAIException, emailproai_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Include API routes
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(emailgen.router, prefix="/api/emailgen", tags=["emailgen"])
app.include_router(campaign.router, prefix="/api/campaign", tags=["campaign"])
app.include_router(followup.router, prefix="/api/followup", tags=["followup"])
app.include_router(history.router, prefix="/api/history", tags=["history"])
app.include_router(payments.router, prefix="/api/payments", tags=["payments"])
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(teams.router, prefix="/api/teams", tags=["teams"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["analytics"])
app.include_router(scheduling.router, prefix="/api/scheduling", tags=["scheduling"])
app.include_router(mobile.router, prefix="/api/mobile", tags=["mobile"])

# Root route
@app.get("/")
def read_root():
    return {"message": "Welcome to EmailProAI", "status": "healthy"}

# Health check
@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": str(datetime.now())}

# Start background scheduler when app launches
@app.on_event("startup")
def startup_event():
    email_logger.info("EmailProAI API starting up...")
    start_scheduler()

@app.on_event("shutdown")
def shutdown_event():
    email_logger.info("EmailProAI API shutting down...")
