#!/bin/bash

echo "================================"
echo "Starting FitMentor"
echo "================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Running setup..."
    ./setup.sh
fi

# Activate virtual environment
source venv/bin/activate

# Start backend server
echo "Starting backend server on http://localhost:5000"
echo "Press Ctrl+C to stop"
echo ""
cd backend
python app.py
