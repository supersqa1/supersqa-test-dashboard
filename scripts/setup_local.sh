#!/bin/bash

# Remove existing virtual environment if it exists
rm -rf venv

# Create new virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip and install build tools
pip install --upgrade pip
pip install --upgrade build

# Install the package in development mode
pip install -e .

# Install development dependencies
pip install -e ".[dev]"

# Set environment variables
export DB_HOST="localhost"
export DB_USER="root"
export DB_PASSWORD="password"
export DB_PORT="3309"
export RESULTS_DIR="./data"
export APP_INSTANCE_DIR="$(pwd)"
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Run the application
cd automationdashboard && python run.py 