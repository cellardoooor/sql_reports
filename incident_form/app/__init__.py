import os
import sys
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from logging.handlers import RotatingFileHandler
import logging

from .config import Config
from .models import db, Incident
from .forms import IncidentForm

def create_app():
    app = Flask(__name__, 
                template_folder='templates',
                static_folder='../static')
    app.config.from_object(Config)
    
    # Logging configuration
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    file_handler = RotatingFileHandler(
        'logs/app.log', 
        maxBytes=1024*1024*10,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    
    if app.config['FLASK_DEBUG']:
        # Additional SQL logging in debug mode
        sql_handler = RotatingFileHandler(
            'logs/sql.log',
            maxBytes=1024*1024*10,
            backupCount=5
        )
        sql_handler.setLevel(logging.DEBUG)
        sql_handler.setFormatter(logging.Formatter(
            '%(asctime)s - SQL - %(message)s'
        ))
        logging.getLogger('pyodbc').addHandler(sql_handler)
        logging.getLogger('pyodbc').setLevel(logging.DEBUG)
    
    from . import routes
    app.register_blueprint(routes.bp)
    
    return app
