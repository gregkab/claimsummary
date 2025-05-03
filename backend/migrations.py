import os
from dotenv import load_dotenv
from app.database import engine
from app.models.models import Base

# Make sure to load environment variables before any database connection
load_dotenv()

def create_tables():
    """Creates all tables defined in the models."""
    try:
        print("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully!")
    except Exception as e:
        print(f"Error creating tables: {str(e)}")
        raise

if __name__ == "__main__":
    create_tables() 