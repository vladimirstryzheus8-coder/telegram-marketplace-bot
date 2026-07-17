import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    # Telegram Bot
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '8876332968:AAHzETdVNXFMbjyyK_JWFMYbTTDfGKqwq2U')
    ADMIN_ID = int(os.getenv('ADMIN_ID', '8517586725'))
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///marketplace.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Flask
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Admin Panel
    ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin123')
    
    # Bank Details
    BANK_NAME = os.getenv('BANK_NAME', 'OPAY')
    ACCOUNT_NUMBER = os.getenv('ACCOUNT_NUMBER', '9016685135')
    ACCOUNT_HOLDER = os.getenv('ACCOUNT_HOLDER', 'TAJUDEEN AL AMEEN AYODEJI')
    
    # Payment Settings
    MIN_DEPOSIT = float(os.getenv('MIN_DEPOSIT', '100'))
    MAX_DEPOSIT = float(os.getenv('MAX_DEPOSIT', '1000000'))
    
    # Server
    FLASK_HOST = os.getenv('FLASK_HOST', '0.0.0.0')
    FLASK_PORT = int(os.getenv('FLASK_PORT', '5000'))
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

config = Config()
