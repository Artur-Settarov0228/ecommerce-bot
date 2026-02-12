import os
from dotenv import load_dotenv
from pathlib import Path

# 🔴 BU JOY ENG MUHIM
BASE_DIR = Path(__file__).resolve().parent

ENV_PATH = BASE_DIR / ".env"

print("DEBUG >>> ENV PATH =", ENV_PATH)
print("DEBUG >>> ENV EXISTS =", ENV_PATH.exists())

load_dotenv(dotenv_path=ENV_PATH)


class Settings:
    TOKEN = os.getenv("BOT_TOKEN")

    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASS = os.getenv("DB_PASS")
    DB_PORT = os.getenv("DB_PORT")
    DB_HOST = os.getenv("DB_HOST")

    ADMIN = [
        int(x) for x in os.getenv("ADMIN", "").split(",") if x
    ]


settings = Settings()

print("DEBUG >>> ADMIN FROM ENV =", os.getenv("ADMIN"))
print("DEBUG >>> ADMIN LIST =", settings.ADMIN)
