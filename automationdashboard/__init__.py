
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
import os

app = Flask(__name__)

# Sett logging config



# set configs
app.config['DATA_STORAGE'] = "database"  # Options are 'database' or 'file'.

if app.config['DATA_STORAGE'] == 'file':
    app.config['RESULTS_DIR'] = os.environ.get("RESULTS_DIR")


app.config['DB_HOST'] = os.environ.get("DB_HOST")
app.config['DB_USER'] = os.environ.get("DB_USER")
app.config['DB_PASSWORD'] = os.environ.get("DB_PASSWORD")
app.config['DB_PORT'] = os.environ.get("DB_PORT")

APP_INSTANCE_DIR = os.environ.get("APP_INSTANCE_DIR")

# Set log file path
log_file_path = f'{APP_INSTANCE_DIR}/logfile.log'

# Create a file handler object
file_handler = RotatingFileHandler(log_file_path, maxBytes=10240, backupCount=10)

# Set the log format
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
))

# Set the log level - change to logging.ERROR for only errors
file_handler.setLevel(logging.DEBUG)

# Add the handler to the Flask app's logger
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.DEBUG)

app.logger.info('Application startup')



from automationdashboard.views import get_results
from automationdashboard.views import post_results
from automationdashboard.views import views
