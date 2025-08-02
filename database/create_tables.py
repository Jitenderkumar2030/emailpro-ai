# database/create_tables.py

from app.db.base import Base
from app.db.session import engine
from app.models import user  # make sure to import all models

# Create all tables in the database
print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("All tables created successfully.")
