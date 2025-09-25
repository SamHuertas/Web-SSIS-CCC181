#!/usr/bin/env python3

import os
import requests
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

print(f"Testing connection to: {url}")
print(f"Using key: {key[:10]}..." if key else "No key found")

# Test 1: Basic HTTP request
try:
    response = requests.get(f"{url}/rest/v1/", headers={
        "apikey": key,
        "Authorization": f"Bearer {key}"
    }, timeout=10)
    print(f"✅ HTTP request successful: {response.status_code}")
except requests.exceptions.ConnectionError as e:
    print(f"❌ Connection error: {e}")
except requests.exceptions.Timeout:
    print("❌ Request timed out")
except Exception as e:
    print(f"❌ Other error: {e}")

# Test 2: Try with Supabase client
try:
    from supabase import create_client
    supabase = create_client(url, key)
    print("✅ Supabase client created successfully")
    
    # Try a simple operation
    result = supabase.table("colleges").select("count", count="exact").execute()
    print(f"✅ Database query successful: {result.count} records")
    
except Exception as e:
    print(f"❌ Supabase client error: {e}")
    print(f"Error type: {type(e).__name__}")