set -x


mysql_prod_volume_path="/root/projects/automation_dashboard/$1/mysql_volume"
PORT=$2
IMAGE_ID=$3


docker run --restart unless-stopped -d --name mysql_$1_automationdashboard -v ${mysql_prod_volume_path}=/var/lib/mysql -e MYSQL_ROOT_PASSWORD=$MYSQL_ROOT_PASSWORD -p $PORT:3306 $IMAGE_ID