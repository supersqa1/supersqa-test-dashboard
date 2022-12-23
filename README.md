# Automation Results Dashboard

## Description
Display's results of automation run. Color coded for PASS/FAIL.
Automation results are created by making POST endpoint api call.
Automation results can be retried with a GET endpoint.


* See 'notes.txt' for more info




## Deployment

- It runs script 'deploy.sh' to deploy the app
- Deployment is done by copying the files (scp) to the server and running gunicorn webserver

## Data Storage
* Depending on the version of the app, data is stored in .json files or in MySQL database
* Database info in ./management


## Environment variables required
### For 'staging' environment
```
STAGING_DB_HOST
STAGING_DB_PORT
STAGING_DB_USER
STAGING_DB_PASSWORD
```

### For 'prod' environment
```
PROD_DB_HOST
PROD_DB_PORT
PROD_DB_USER
PROD_DB_PASSWORD
```
-  In GitLab these variables are set as CI/CD variables


