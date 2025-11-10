#!/bin/bash

echo "================================"
echo "FitMentor Setup Script"
echo "================================"
echo ""

# Check Python version
if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
    PIP_CMD=pip3
elif command -v python &> /dev/null; then
    PYTHON_CMD=python
    PIP_CMD=pip
else
    echo "Error: Python not found. Please install Python 3.8+"
    exit 1
fi

echo "Using Python: $($PYTHON_CMD --version)"
echo ""

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    $PYTHON_CMD -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
$PIP_CMD install --upgrade pip

# Install dependencies
echo ""
echo "Installing dependencies (this may take a few minutes)..."
$PIP_CMD install -r requirements.txt

echo ""
echo "================================"
echo "✓ Setup complete!"
echo "================================"
echo ""
echo "To start the application:"
echo "  1. Activate environment: source venv/bin/activate"
echo "  2. Start backend: python backend/app.py"
echo "  3. Open frontend/index.html in your browser"
echo ""
