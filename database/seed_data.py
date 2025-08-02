from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash  # <-- real hashing from your app

def seed_users():
    db: Session = SessionLocal()

    existing_user = db.query(User).filter(User.email == "admin@example.com").first()
    if existing_user:
        print("✅ Test user already exists.")
        db.close()
        return

    user = User(
        email="admin@example.com",
        hashed_password=get_password_hash("admin123"),  # correct hash
        full_name="Admin User",
        is_active=True,
        credits=10
    )
    db.add(user)
    db.commit()
    db.close()
    print("✅ Test user seeded successfully.")

if __name__ == "__main__":
    seed_users()
