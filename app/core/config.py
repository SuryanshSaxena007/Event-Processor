import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
RABBITMQ_URL = os.getenv("RABBITMQ_URL")
SECRET_KEY    = os.getenv("SECRET_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES = 30