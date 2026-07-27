import os
from dotenv import load_dotenv
from sqlalchemy import URL

load_dotenv()

class Config:

    TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
    TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")

    SQLALCHEMY_DATABASE_URI = URL.create(
        drivername=os.getenv("DB_DRIVER"),
        username=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        database=os.getenv("DB_NAME"),
    )

    DB_SSL_CA_PATH = os.path.join(os.path.dirname(__file__), "ca.pem")           # Works regardless of run from any directory (returns "that folder + ca.pem")
    SQLALCHEMY_ENGINE_OPTIONS = {
        "connect_args": {
            "ssl": {
                "ca": DB_SSL_CA_PATH
            }
        }
    }

    SQLALCHEMY_TRACK_MODIFICATIONS = False


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")