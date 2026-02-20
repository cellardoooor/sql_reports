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
                conn_str = (
                    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                    f"SERVER={current_app.config['SQL_SERVER']};"
                    f"DATABASE={current_app.config['SQL_DATABASE']};"
                    f"UID={current_app.config['SQL_USER']};"
                    f"PWD={current_app.config['SQL_PASSWORD']};"
                    f"TrustServerCertificate=yes;"
                )
                logger.info(f"Connecting to SQL Server: {current_app.config['SQL_SERVER']}")
                self.conn = pyodbc.connect(conn_str)
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
        logger.info(f"=== START Incident.create ===")
        logger.info(f"Input data: {data}")
        
        conn = db.get_connection()
        cursor = conn.cursor()
        
        try:
            # Обрабатываем необязательные поля
            logger.info(f"Step 1: Processing validity_days")
            validity_days = data.get('validity_days')
            logger.info(f"  validity_days value: {validity_days}, type: {type(validity_days).__name__}")
            
            validity_hours = validity_days * 24 if validity_days else None
            logger.info(f"Step 2: validity_hours = {validity_hours}, type: {type(validity_hours).__name__}")
            
            logger.info(f"Step 3: Processing event_datetime")
            event_datetime_raw = data.get('event_datetime')
            logger.info(f"  event_datetime_raw: {event_datetime_raw}, type: {type(event_datetime_raw).__name__}")
            
            if event_datetime_raw and 'T' in str(event_datetime_raw):
                event_datetime_str = str(event_datetime_raw).replace('T', ' ') + ':00'
                logger.info(f"Step 4a: Converted datetime: {event_datetime_str}")
            else:
                event_datetime_str = str(event_datetime_raw)
                logger.info(f"Step 4b: Using raw datetime: {event_datetime_str}")
            
            logger.info(f"Step 5: Processing fio")
            fio = data.get('fio')
            logger.info(f"  fio: {fio}, type: {type(fio).__name__}")
            fio_str = str(fio or '')
            logger.info(f"  fio_str: {fio_str}, type: {type(fio_str).__name__}")
            
            logger.info(f"Step 6: Processing tag")
            tag = data.get('tag')
            logger.info(f"  tag: {tag}, type: {type(tag).__name__}")
            tag_str = str(tag or '')
            logger.info(f"  tag_str: {tag_str}, type: {type(tag_str).__name__}")
            
            logger.info(f"Step 7: Processing event_description")
            event_desc = data.get('event_description')
            logger.info(f"  event_description: {event_desc}, type: {type(event_desc).__name__}")
            event_desc_str = str(event_desc or '')
            logger.info(f"  event_desc_str: {event_desc_str}, type: {type(event_desc_str).__name__}")
            
            logger.info(f"Step 8: Processing engineer_actions")
            eng_actions = data.get('engineer_actions')
            logger.info(f"  engineer_actions: {eng_actions}, type: {type(eng_actions).__name__}")
            eng_actions_str = str(eng_actions or '')
            logger.info(f"  eng_actions_str: {eng_actions_str}, type: {type(eng_actions_str).__name__}")
            
            logger.info(f"Step 9: Creating params tuple")
            params = (
                fio_str,           # NVARCHAR
                event_datetime_str, # DATETIME2 как строка
                tag_str,           # NVARCHAR
                validity_hours,    # INT (может быть None)
                event_desc_str,    # NVARCHAR(MAX)
                eng_actions_str    # NVARCHAR(MAX)
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
            
        except Exception as e:
            conn.rollback()
            logger.error(f"Error creating event: {e}")
            logger.error(f"Error type: {type(e).__name__}")
            import traceback
            logger.error(f"Traceback:\n{traceback.format_exc()}")
            raise
        finally:
            cursor.close()
