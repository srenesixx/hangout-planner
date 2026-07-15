import sys
import os

# Application Settings
APP_TITLE = "Hangout Planner — Aplikasi Budget Nongkrong"
WINDOW_SIZE = "1100x700"
MIN_WINDOW_SIZE = (1050, 650)

# Paths Configuration
if getattr(sys, 'frozen', False):
    # When running as an executable, place user files in the same directory as the executable
    BASE_DIR = os.path.dirname(sys.executable)
else:
    # When running in development, place user files in the project root
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DB_FILE = os.path.join(BASE_DIR, 'hangout_planner.db')
