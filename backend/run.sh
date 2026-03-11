#!/bin/bash

echo "===================================="
echo "AI Software Engineer Agent - Backend"
echo "===================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo ""
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo ""

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "WARNING: .env file not found!"
    echo "Please copy .env.example to .env and configure your API keys"
    echo ""
    exit 1
fi

# Install/upgrade dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
echo ""

# Create necessary directories
mkdir -p data/chroma_db
mkdir -p data/projects
mkdir -p logs

# Run the application
echo "Starting Flask application..."
echo "Server will be available at http://localhost:5000"
echo "Press Ctrl+C to stop"
echo ""
python app.py
