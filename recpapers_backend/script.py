import os
import sys
from dotenv import load_dotenv

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

load_dotenv()  # optional: loads .env file if present

DATABASE_URL = os.getenv("DATABASE_URL")
# DATABASE_URL = str(DATABASE_URL).replace('postgresql',"postgresql+psycopg2")
if not DATABASE_URL:
    print("ERROR: set DATABASE_URL environment variable (e.g. postgresql+psycopg2://user:pass@host:port/dbname)")
    sys.exit(1)

# create engine (SQLAlchemy URL should include driver, e.g. postgresql+psycopg2://...)
engine = create_engine(DATABASE_URL, future=True)
Session = sessionmaker(bind=engine, future=True)

def fetch_rows(sql: str):
    with engine.connect() as conn:
        result = conn.execute(text(sql))
        rows = result.fetchall()
    return rows

if __name__ == "__main__":
    table = sys.argv[1] if len(sys.argv) > 1 else "papers"
    sql = "SHOW TABLES;"
    try:
        rows = fetch_rows(sql)
        for row in rows:
            # convert ResultRow to dict for nicer printing
            print(dict(row._mapping))
    finally:
        engine.dispose()