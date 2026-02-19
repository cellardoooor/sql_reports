#!/usr/bin/env python3
"""
Скрипт сборки исполняемого файла через PyInstaller
"""

import PyInstaller.__main__
import os
import sys
import shutil

def build():
    """Сборка исполняемого файла"""
    
    # Очистка предыдущих сборок
    for folder in ['build', 'dist']:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"Удалена папка {folder}")
    
    # Параметры сборки
    args = [
        'run.py',                           # Главный файл
        '--name=incident_form',             # Имя исполняемого файла
        '--onefile',                        # Один файл
        '--windowed',                       # Без консоли (можно убрать для отладки)
        '--add-data=app/templates:app/templates',  # Шаблоны
        '--add-data=static/css:static/css',        # CSS
        '--add-data=static/js:static/js',          # JS
        '--add-data=.env:.',                # Файл окружения
        '--hidden-import=flask',
        '--hidden-import=flask_wtf',
        '--hidden-import=wtforms',
        '--hidden-import=pyodbc',
        '--hidden-import=waitress',
        '--hidden-import=dotenv',
        '--collect-all=flask',
        '--collect-all=flask_wtf',
        '--collect-all=wtforms',
        '--clean',                          # Очистка кэша
        '--noconfirm',                      # Без подтверждений
    ]
    
    # Дополнительные скрытые импорты для Windows
    if sys.platform == 'win32':
        args.extend([
            '--hidden-import=win32timezone',
        ])
    
    print("Начинаем сборку...")
    print(f"Параметры: {' '.join(args)}")
    
    PyInstaller.__main__.run(args)
    
    print("\nСборка завершена!")
    print("Исполняемый файл: dist/incident_form.exe")
    
    # Создание папки для логов
    if not os.path.exists('dist/logs'):
        os.makedirs('dist/logs')
        print("Создана папка dist/logs")

if __name__ == '__main__':
    build()
