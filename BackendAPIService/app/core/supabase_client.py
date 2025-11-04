import os
from supabase import create_client, Client  # type: ignore

_SUPABASE_URL = os.getenv("SUPABASE_URL")
_SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not _SUPABASE_URL or not _SUPABASE_KEY:
    # Log a clear warning on import; actual app startup should validate and fail fast if required
    print("WARNING: SUPABASE_URL or SUPABASE_KEY not set. Supabase client may not initialize correctly.")

def get_supabase_client() -> Client:
    """
    Returns a Supabase client using server-side credentials.
    Use service role key if privileged operations are needed; otherwise anon key.
    """
    if not _SUPABASE_URL or not _SUPABASE_KEY:
        raise RuntimeError("Missing SUPABASE_URL or SUPABASE_KEY environment variables.")
    return create_client(_SUPABASE_URL, _SUPABASE_KEY)
