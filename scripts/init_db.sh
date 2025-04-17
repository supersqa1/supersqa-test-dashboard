#!/bin/bash

# Create database and table
mysql -u root -ppassword << EOF
CREATE DATABASE IF NOT EXISTS automationdashboard;
USE automationdashboard;

CREATE TABLE IF NOT EXISTS test_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    test_group_name VARCHAR(255) NOT NULL,
    result_status VARCHAR(50) NOT NULL,
    number_of_passed_tests INT NOT NULL,
    number_of_failed_tests INT NOT NULL,
    start_time DATETIME NOT NULL,
    end_time DATETIME NOT NULL
);
EOF 