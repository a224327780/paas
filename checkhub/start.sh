#!/bin/bash

echo "🎯 Starting CheckHub..."

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt -q

echo "Starting application..."
python run.py
