set -x

# Example Command:
  # $ bash mysql_start_automationdashboard.sh prod 3308 7484689f290f


mysql_volume_path="/root/database_volumes/$1/mysql_volume"
PORT=$2
IMAGE_ID=$3

mkdir -p $mysql_volume_path

docker run --restart unless-stopped -d --name mysql_$1_automationdashboard -v ${mysql_volume_path}=/var/lib/mysql -e MYSQL_ROOT_PASSWORD=$MYSQL_ROOT_PASSWORD -p $PORT:3306 $IMAGE_ID