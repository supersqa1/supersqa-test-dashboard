#!/bin/bash

# Remove existing virtual environment
rm -rf venv

# Create new virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip and install dependencies
pip install --upgrade pip
pip install "fastapi>=0.109.0" "uvicorn[standard]>=0.27.0" "jinja2>=3.1.0" "python-multipart>=0.0.6" "aiofiles>=23.2.1" "python-dotenv>=1.0.0"

# Create templates directory if it doesn't exist
mkdir -p templates

# Run the application
python -m uvicorn main:app --reload --port 8000 