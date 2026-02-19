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
            validity_hours = data['validity_days'] * 24 if data['validity_days'] else None
            
            cursor.execute("""
                INSERT INTO incidents (fio, event_datetime, tag, validity_hours, event_description, engineer_actions)
                VALUES (?, ?, ?, ?, ?, ?);
                SELECT SCOPE_IDENTITY();
            """, (
                data['fio'],
                data['event_datetime'],
                data['tag'],
                validity_hours,
                data['event_description'] or '',
                data['engineer_actions'] or ''
            ))
            
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
