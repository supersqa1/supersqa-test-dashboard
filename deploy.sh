set -x

chmod 400 ${DRP3_KEY}
ssh -o StrictHostKeyChecking=no -i ${DRP3_KEY} "root@198.199.111.109" "mkdir -p ${APP_INSTANCE_DIR}"
scp -o StrictHostKeyChecking=no -i ${DRP3_KEY} -r ./automationdashboard root@198.199.111.109:${APP_INSTANCE_DIR}
scp -o StrictHostKeyChecking=no -i ${DRP3_KEY} -r ./requirements.txt root@198.199.111.109:${APP_INSTANCE_DIR}
ssh -o StrictHostKeyChecking=no -i $DRP3_KEY "root@198.199.111.109" "python3 -m venv ${VIRTUAL_ENVIRONMENT}"
ssh -o StrictHostKeyChecking=no -i $DRP3_KEY "root@198.199.111.109" "${VIRTUAL_ENVIRONMENT}/bin/python -m pip install -r ${APP_INSTANCE_DIR}/requirements.txt"
ssh -o StrictHostKeyChecking=no -i $DRP3_KEY "root@198.199.111.109" "cd ${APP_INSTANCE_DIR}/automationdashboard && export PYTHONPATH=${APP_INSTANCE_DIR} && source variables.sh && ${VIRTUAL_ENVIRONMENT}/bin/python -m gunicorn --workers 1 --bind 127.0.0.1:${PORT} automationdashboard:app --daemon --reload"
