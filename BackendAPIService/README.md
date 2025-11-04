# BackendAPIService Supabase Setup

Environment variables:
- SUPABASE_URL: https://<project>.supabase.co
- SUPABASE_KEY: Service role key (preferred for backend) or anon key for limited operations

Optional:
- SITE_URL: Base site URL for composing redirects if your backend triggers auth flows

Python dependency:
- supabase: Ensure your Python environment has the supabase client installed (e.g., pip install supabase)

Usage:
- Import the client factory:
  from app.core.supabase_client import get_supabase_client
- Then:
  supabase = get_supabase_client()
