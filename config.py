import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Telegram Bot settings
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN', '7022660975:AAFZrBnJBgB45VxAN1VHDOBgOgCc0QqdIHo')
    WEBAPP_URL = os.getenv('WEBAPP_URL', 'https://finance-bot-z9rl.onrender.com')
    
    # Database settings
    DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://finance_bot_user:TF7ExYjPV9LsexpjvbL0kU9nwKJiH6c1@dpg-d2a0ha6r433s739uum4g-a/finance_bot_2m37')
    
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Supported currencies
    SUPPORTED_CURRENCIES = ['BYN', 'RUB', 'USD']
    
    # Default currency
    DEFAULT_CURRENCY = 'BYN' 