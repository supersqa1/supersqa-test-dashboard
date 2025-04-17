import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
import os

app = Flask(__name__)

# set configs
app.config['DATA_STORAGE'] = "database"  # Options are 'database' or 'file'.

if app.config['DATA_STORAGE'] == 'file':
    app.config['RESULTS_DIR'] = os.environ.get("RESULTS_DIR")

app.config['DB_HOST'] = os.environ.get("DB_HOST")
app.config['DB_USER'] = os.environ.get("DB_USER")
app.config['DB_PASSWORD'] = os.environ.get("DB_PASSWORD")
app.config['DB_PORT'] = os.environ.get("DB_PORT")

# Configure logging
# Create logs directory if it doesn't exist
if not os.path.exists('logs'):
    os.mkdir('logs')

# Configure file handler
file_handler = RotatingFileHandler('logs/automationdashboard.log', maxBytes=10240, backupCount=10)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
))
file_handler.setLevel(logging.INFO)

# Configure app logger
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)
app.logger.info('Automation Dashboard startup')

# Import views after app initialization to avoid circular imports
from automationdashboard.views import get_results
from automationdashboard.views import post_results
from automationdashboard.views import views
