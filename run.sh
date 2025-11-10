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

# Force CPU mode (avoids GPU/CUDA issues)
export CUDA_VISIBLE_DEVICES='-1'
export TF_CPP_MIN_LOG_LEVEL='2'

# Start backend server
echo "Starting backend server on http://localhost:5000"
echo "Using CPU mode (fast enough for this app)"
echo "Press Ctrl+C to stop"
echo ""
cd backend
python app.py
