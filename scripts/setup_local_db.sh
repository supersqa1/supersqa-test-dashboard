#!/bin/bash

# Create directory for MySQL data
mkdir -p ./data/mysql_volume

# Run MySQL container
docker run --restart unless-stopped -d \
  --name mysql_local_automationdashboard \
  -v $(pwd)/data/mysql_volume:/var/lib/mysql \
  -e MYSQL_ROOT_PASSWORD=password \
  -p 3309:3306 \
  mysql:8.0

# Wait for MySQL to be ready
echo "Waiting for MySQL to start..."
sleep 30

# Create database and table
docker exec mysql_local_automationdashboard mysql -uroot -ppassword -e "
CREATE DATABASE IF NOT EXISTS \`automationdashboard\` DEFAULT CHARACTER SET utf8;
USE \`automationdashboard\`;
$(cat management/sql/create_table.sql)
" 