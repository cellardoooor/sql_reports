import pyodbc
from flask import current_app
import logging

logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        self.conn = None
    
    def get_connection(self):
        if self.conn is None or self.conn.closed:
            try:
                self.conn = pyodbc.connect(current_app.config['DATABASE_CONNECTION_STRING'])
                logger.info("Database connection established")
            except pyodbc.Error as e:
                logger.error(f"Database connection error: {e}")
                raise
        return self.conn
    
    def close(self):
        if self.conn and not self.conn.closed:
            self.conn.close()
            logger.info("Database connection closed")

db = Database()

class Incident:
    @staticmethod
    def create(data):
        conn = db.get_connection()
        cursor = conn.cursor()
        
        try:
            # Обрабатываем необязательные поля
            validity_hours = data.get('validity_days') * 24 if data.get('validity_days') else None
            
            # event_datetime теперь всегда строка
            event_datetime_str = str(data.get('event_datetime') or '')
            
            params = (
                str(data.get('fio') or ''),           # NVARCHAR
                event_datetime_str,                    # DATETIME2 как строка
                str(data.get('tag') or ''),           # NVARCHAR
                validity_hours,                        # INT (может быть None)
                str(data.get('event_description') or ''),   # NVARCHAR(MAX)
                str(data.get('engineer_actions') or '')     # NVARCHAR(MAX)
            )
            
            logger.info(f"SQL params: {params}")
            logger.info(f"SQL param types: {[type(p).__name__ for p in params]}")
            
            cursor.execute("""
                INSERT INTO incidents (fio, event_datetime, tag, validity_hours, event_description, engineer_actions)
                VALUES (?, ?, ?, ?, ?, ?);
                SELECT SCOPE_IDENTITY();
            """, params)
            
            incident_id = cursor.fetchone()[0]
            conn.commit()
            logger.info(f"Event created with ID: {incident_id}")
            return incident_id
            
        except pyodbc.Error as e:
            conn.rollback()
            logger.error(f"Error creating event: {e}")
            raise
        finally:
            cursor.close()
