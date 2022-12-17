set -x

# Deploys the application to the provided ip address (Ubuntu server on digitalocean (VPS))
# Expects certain variables to be set

IP=198.199.111.109
REMOTE_USER=root

STAGING_DB_HOST=foobar

# database info
if [ ${ENVIRONMENT} == 'staging' ]; then

  DB_HOST=$STAGING_DB_HOST
  DB_PORT=$STAGING_DB_PORT
  DB_USER=$STAGING_DB_USER
  DB_PASSWORD=$STAGING_DB_PASSWORD
elif [ ${ENVIRONMENT} == 'staging' ]; then
    DB_HOST=$PROD_DB_HOST
    DB_PORT=$PROD_DB_PORT
    DB_USER=$PROD_DB_USER
    DB_PASSWORD=$PROD_DB_PASSWORD
else
  echo "Unknown value '$ENVIRONMENT' for variable 'ENVIRONMENT'"
  exit 1
fi



# TODO: just do one ssh connection and multiple commands
chmod 400 ${DRP3_KEY}
ssh -o StrictHostKeyChecking=no -i ${DRP3_KEY} "$REMOTE_USER@$IP" "mkdir -p ${APP_INSTANCE_DIR}"
scp -o StrictHostKeyChecking=no -i ${DRP3_KEY} -r ./automationdashboard $REMOTE_USER@$IP:${APP_INSTANCE_DIR}
scp -o StrictHostKeyChecking=no -i ${DRP3_KEY} -r ./requirements.txt $REMOTE_USER@$IP:${APP_INSTANCE_DIR}
ssh -o StrictHostKeyChecking=no -i $DRP3_KEY "$REMOTE_USER@$IP" "python3 -m venv ${VIRTUAL_ENVIRONMENT}"
ssh -o StrictHostKeyChecking=no -i $DRP3_KEY "$REMOTE_USER@$IP" "${VIRTUAL_ENVIRONMENT}/bin/python -m pip install -r ${APP_INSTANCE_DIR}/requirements.txt"
ssh -o StrictHostKeyChecking=no -i $DRP3_KEY "$REMOTE_USER@$IP" "cd ${APP_INSTANCE_DIR}/automationdashboard \
&& export PYTHONPATH=${APP_INSTANCE_DIR} \
&& export ENVIRONMENT=${ENVIRONMENT} \
&& export DB_HOST=${DB_HOST} \
&& export DB_PORT=${DB_PORT} \
&& export DB_USER=${DB_USER} \
&& export DB_PASSWORD=${DB_PASSWORD} \
&& source variables.sh \
&& ${VIRTUAL_ENVIRONMENT}/bin/python -m gunicorn --workers 1 --bind 127.0.0.1:${PORT} automationdashboard:app --daemon --reload"
