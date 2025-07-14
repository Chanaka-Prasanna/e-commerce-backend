# test_db_connection.py
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from app.database import engine

def test_connection():
    try:
        # connect() gives you a Connection
        with engine.connect() as conn:
            # wrap the SQL in text()
            conn.execute(text("SELECT 1"))
        print("✅ DB connection successful!")
    except SQLAlchemyError as err:
        print("❌ DB connection failed:", err)

if __name__ == "__main__":
    test_connection()
