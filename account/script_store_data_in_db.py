import os
import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor, execute_values
from dotenv import load_dotenv
import json

load_dotenv()
DATABASE_URL = os.environ.get("DATABASE_URL")
def update_data():

    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor(cursor_factory=RealDictCursor)

        # list databases
        # cur.execute("SELECT datname FROM pg_database WHERE datistemplate = false;")
        # databases = [r[0] for r in cur.fetchall()]
        # print("Databases:", databases)

        # list user tables (exclude system schemas)
        # cur.execute("""
        #     SELECT table_schema, table_name
        #     FROM information_schema.tables
        #     WHERE table_type = 'BASE TABLE'
        #       AND table_schema NOT IN ('pg_catalog','information_schema')
        #     ORDER BY table_schema, table_name;
        # """)
        # tables = cur.fetchall()
        # print("Tables:")
        # for schema, name in tables:
        #     print(f"  {schema}.{name}")

        cur.execute("SELECT * From recpaper_app_project;")
        users = cur.fetchall()
        print("users:", users)

        print("-----"*10)
        # for user in users:
        #     for key,item in user.items():
        #         print(f"{key}: {item}")

        # cur.execute("SELECT * From account_user_profile;")
        # db_version = cur.fetchone()
        user_data=None
        cols=[]
        values=[]
        with open('recpaper_app_project_log.json', 'r') as f:
            data = f.read()
            user_data = json.loads(data)
            print("Data from recpaper_app_projects_log.json:", type(user_data))

        cols = user_data[0].keys()
        for user in user_data:
            values.append([user.get(col) for col in cols])
            # values = tuple(values)
            # cur.execute(f'INSERT INTO account_user ({", ".join(cols)}) VALUES %s', (values,))
        print("Columns:", cols)
        print("Values:", values[0])
        cols_sql = sql.SQL(", ").join([sql.Identifier(c) for c in cols])
        insert_sql = sql.SQL("INSERT INTO recpaper_app_project_log ({cols}) VALUES %s").format(cols=cols_sql)

        execute_values(cur, insert_sql.as_string(conn), values)
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"An error occurred: {e}")
        
if __name__ == "__main__":
    # update_data()
    pass