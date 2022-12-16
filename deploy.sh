set -x

# Deploys the application to the provided ip address
# Expects certain variables to be set

IP=198.199.111.109
REMOTE_USER=root

# TODO: just do one ssh connection and multiple commands
chmod 400 ${DRP3_KEY}
ssh -o StrictHostKeyChecking=no -i ${DRP3_KEY} "$REMOTE_USER@$IP" "mkdir -p ${APP_INSTANCE_DIR}"
scp -o StrictHostKeyChecking=no -i ${DRP3_KEY} -r ./automationdashboard $REMOTE_USER@$IP:${APP_INSTANCE_DIR}
scp -o StrictHostKeyChecking=no -i ${DRP3_KEY} -r ./requirements.txt $@REMOTE_USER$IP:${APP_INSTANCE_DIR}
ssh -o StrictHostKeyChecking=no -i $DRP3_KEY "$REMOTE_USER@$IP" "python3 -m venv ${VIRTUAL_ENVIRONMENT}"
ssh -o StrictHostKeyChecking=no -i $DRP3_KEY "$REMOTE_USER@$IP" "${VIRTUAL_ENVIRONMENT}/bin/python -m pip install -r ${APP_INSTANCE_DIR}/requirements.txt"
ssh -o StrictHostKeyChecking=no -i $DRP3_KEY "$REMOTE_USER@$IP" "cd ${APP_INSTANCE_DIR}/automationdashboard && export PYTHONPATH=${APP_INSTANCE_DIR} && source variables.sh && ${VIRTUAL_ENVIRONMENT}/bin/python -m gunicorn --workers 1 --bind 127.0.0.1:${PORT} automationdashboard:app --daemon --reload"
