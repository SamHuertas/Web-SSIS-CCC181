import psycopg2
from psycopg2.extras import RealDictCursor
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

def get_connection():
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)

def get_supabase_client():
    return create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)