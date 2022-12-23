
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





from automationdashboard.views import get_results
from automationdashboard.views import post_results
from automationdashboard.views import views
