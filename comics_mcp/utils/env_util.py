import os
from dotenv import load_dotenv

load_dotenv()

def get_env_var(name: str, default: str = None) -> str:
    value = os.getenv(name, default)
    if value is None:
        raise EnvironmentError(f"Missing required environment variable: {name}")
    return value

def get_comicvine_api_key() -> str:
    """Get Comic Vine API key from environment variables"""
    api_key = get_env_var("COMICVINE_API_KEY")
    if not api_key:
        raise ValueError("Missing COMICVINE_API_KEY in environment variables")
    return api_key