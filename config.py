import os

API_HOST = os.getenv('API_HOST', '127.0.0.1')
API_PORT = int(os.getenv('API_PORT', 8000))
DB_URL = os.getenv('DB_URL', "sqlite+aiosqlite:///./persons.db")
