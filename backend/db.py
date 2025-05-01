from supabase import create_client
from .config import settings

supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

def get_user(user_id: str):
    response = supabase.table("users").select("*").eq("id", user_id).single().execute()
    return response.data

def get_challenge(challenge_id: str):
    response = supabase.table("challenges").select("*").eq("id", challenge_id).single().execute()
    return response.data

def create_challenge(data: dict):
    response = supabase.table("challenges").insert(data).execute()
    return response.data

def create_submission(data: dict):
    response = supabase.table("submissions").insert(data).execute()
    return response.data

def get_submissions_by_student(student_id: str):
    response = supabase.table("submissions").select("*").eq("student_id", student_id).execute()
    return response.data
