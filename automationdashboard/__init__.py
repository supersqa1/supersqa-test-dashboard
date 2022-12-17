
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

print("xxxxxxxxxxx")
import pprint
pprint.pprint(app.config, indent=4)
print("xxxxxxxxxxx")
# environment = os.environ.get("ENVIRONMENT")
# assert environment.lower() in ('staging', 'prod'), f"Env variable 'ENVIRONMENT' must be set to 'staging' or 'prod'."
# app.config['DB_HOST'] = os.environ.get("STAGING_DB_HOST") if environment.lower() == 'staging' else os.environ.get("PROD_DB_HOST")
# app.config['DB_USER'] = os.environ.get("STAGING_DB_USER") if environment.lower() == 'staging' else os.environ.get("PROD_DB_USER")
# app.config['DB_PASSWORD'] = os.environ.get("STAGING_DB_PASSWORD") if environment.lower() == 'staging' else os.environ.get("PROD_DB_PASSWORD")
# app.config['DB_PORT'] = os.environ.get("STAGING_DB_PORT") if environment.lower() == 'staging' else os.environ.get("PROD_DB_PORT")







from automationdashboard.views import post_results
from automationdashboard.views import views
