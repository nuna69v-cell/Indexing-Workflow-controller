import os
from dotenv import load_dotenv

def load_env():
    load_dotenv()
    return {
        'DB_URL': os.getenv('DB_URL'),
        'API_KEY': os.getenv('API_KEY')
    }
