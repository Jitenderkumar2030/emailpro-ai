# backend/app/core/scheduler.py

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from pytz import utc
import logging

from app.services.followup_service import run_followups

# Initialize the scheduler with a supported timezone (pytz)
scheduler = BackgroundScheduler(timezone=utc)
logging.getLogger('apscheduler').setLevel(logging.DEBUG)

def start_scheduler():
    scheduler.add_job(
        run_followups,
        trigger=IntervalTrigger(days=1, timezone=utc),
        id="daily_followup_job",
        replace_existing=True
    )
    scheduler.start()
