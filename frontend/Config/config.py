import os

class Config:
    BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")
