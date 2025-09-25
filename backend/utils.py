import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

class SupabaseManager:
    def __init__(self):
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_KEY")

        if not self.url or not self.key:
            raise ValueError("Supabase credentials are missing. Check your .env file.")

        self.client: Client = create_client(self.url, self.key)

    def get_client(self) -> Client:
        return self.client




