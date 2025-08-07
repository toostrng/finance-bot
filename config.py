import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Telegram Bot settings
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
    WEBAPP_URL = os.getenv('WEBAPP_URL', 'https://your-domain.com')
    
    # Database settings
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///finance_bot.db')
    
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Supported currencies
    SUPPORTED_CURRENCIES = ['BYN', 'RUB', 'USD']
    
    # Default currency
    DEFAULT_CURRENCY = 'BYN' 