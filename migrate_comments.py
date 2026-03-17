import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()
db_url = os.environ.get('DATABASE_URL')
if not db_url:
    print("No DATABASE_URL found.")
    exit(1)

if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

engine = create_engine(db_url)

with engine.connect() as conn:
    print("Altering comment table to add parent_id...")
    try:
        conn.execute(text("""
            ALTER TABLE comment ADD COLUMN parent_id INTEGER REFERENCES comment(id) ON DELETE CASCADE;
        """))
        conn.commit()
        print("comment table updated!")
    except Exception as e:
        if "duplicate column name" in str(e).lower() or "already exists" in str(e).lower():
            print("Column parent_id already exists.")
        else:
            print("Error altering table:", e)
