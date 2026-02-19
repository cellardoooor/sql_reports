import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQL_SERVER = os.getenv('SQL_SERVER', 'localhost')
    SQL_DATABASE = os.getenv('SQL_DATABASE', 'incidents_db')
    SQL_USER = os.getenv('SQL_USER', 'app_user')
    SQL_PASSWORD = os.getenv('SQL_PASSWORD', '')
    FLASK_PORT = int(os.getenv('FLASK_PORT', 5000))
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
    
    @property
    def DATABASE_CONNECTION_STRING(self):
        return (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={self.SQL_SERVER};"
            f"DATABASE={self.SQL_DATABASE};"
            f"UID={self.SQL_USER};"
            f"PWD={self.SQL_PASSWORD};"
            f"TrustServerCertificate=yes;"
        )
