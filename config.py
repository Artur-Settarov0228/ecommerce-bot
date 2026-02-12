from dotenv import load_dotenv
import os

load_dotenv()

class Settings:   
    TOKEN = os.getenv("BOT_TOKEN")
    DB_NAME= os.getenv("DB_NAME")
    DB_USER= os.getenv("DB_USER")
    DB_PASS= os.getenv("DB_PASS")
    DB_PORT= os.getenv("DB_PORT")
    DB_HOST= os.getenv("DB_HOST")
    ADMIN= os.getenv("ADMIN")
        
settings = Settings()