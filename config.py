import os

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
host = os.getenv("PGHOST")
admin_id = os.getenv("ADMIN_ID")
PG_USER = os.getenv("PG_USER")
PG_PASS = os.getenv("PG_PASS")

