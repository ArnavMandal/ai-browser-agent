from supabase import create_client, Client

url = "https://rxgcxatjkgbedoajnvlr.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ4Z2N4YXRqa2diZWRvYWpudmxyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDQ0OTM1NTQsImV4cCI6MjA2MDA2OTU1NH0.E3MqSTPRKOYAUR-VMIHAA35Shvka1WKLqC0fMUNtBXc"  # paste from your dashboard

supabase: Client = create_client(url, key)

user_count = supabase.table("your_table").select("*").execute()
print("🧪 Connected to Supabase. Users table rows:", len(user_count.data))