# backend/init_db.py
from app.db.base import Base
from app.db.session import engine
from app.models import user, email, campaign, followup

def init():
    print("🔧 Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created.")

if __name__ == "__main__":
    init()
