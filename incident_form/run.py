#!/usr/bin/env python3
"""
Точка входа для разработки и production
"""

import os
import sys

# Добавляем папку app в путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.config import Config

def main():
    app = create_app()
    config = Config()
    
    if config.FLASK_DEBUG:
        # Режим разработки
        app.run(
            host='0.0.0.0',
            port=config.FLASK_PORT,
            debug=True
        )
    else:
        # Production режим с Waitress
        try:
            from waitress import serve
            print(f"Starting server on port {config.FLASK_PORT}...")
            serve(
                app,
                host='0.0.0.0',
                port=config.FLASK_PORT,
                threads=4
            )
        except ImportError:
            # Fallback на Flask development server
            print("Warning: Waitress not installed, using Flask development server")
            app.run(
                host='0.0.0.0',
                port=config.FLASK_PORT,
                debug=False
            )

if __name__ == '__main__':
    main()
