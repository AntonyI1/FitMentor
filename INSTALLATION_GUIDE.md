# FitMentor Installation Guide

## Current Status

✓ Code structure is correct
✓ All files in place
✓ 5 API endpoints defined
✗ Dependencies need to be installed

## What You Need to Install

### Option 1: Automatic Setup (Recommended)

```bash
cd /home/tony/code/FitMentor
./setup.sh
```

This installs everything automatically.

### Option 2: Manual Installation

```bash
cd /home/tony/code/FitMentor

# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies (this takes 5-10 minutes)
pip install flask==3.0.0
pip install flask-cors==4.0.0
pip install numpy==1.24.3
pip install tensorflow==2.15.0
pip install torch==2.1.0
pip install torchvision==0.16.0
```

### Option 3: Minimal Install (Just to Test)

If you want to test quickly without ML:

```bash
pip install flask flask-cors
```

Then modify `backend/app.py` to comment out ML model initialization (lines 17-19).

## Running After Installation

```bash
# Terminal 1: Start backend
cd /home/tony/code/FitMentor/backend
source ../venv/bin/activate  # If using virtual env
python3 app.py

# Terminal 2: Start frontend
cd /home/tony/code/FitMentor/frontend
python3 -m http.server 8000
```

Open browser: **http://localhost:8000**

## Verification Checklist

After installation, verify:

```bash
# Check Python
python3 --version  # Should be 3.8+

# Check pip
pip --version

# Check Flask installed
python3 -c "import flask; print(f'Flask {flask.__version__}')"

# Check TensorFlow installed
python3 -c "import tensorflow as tf; print(f'TensorFlow {tf.__version__}')"

# Check PyTorch installed
python3 -c "import torch; print(f'PyTorch {torch.__version__}')"
```

## Common Issues

### Issue: "No module named pip"
**Solution:** Install pip first:
```bash
sudo apt-get update
sudo apt-get install python3-pip
```

### Issue: "No module named 'flask'"
**Solution:** Install dependencies:
```bash
pip install -r requirements.txt
```

### Issue: TensorFlow/PyTorch too slow to install
**Solution:** Install CPU-only versions (much smaller):
```bash
pip install tensorflow-cpu
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

### Issue: "Port 5000 already in use"
**Solution:** Kill existing process:
```bash
lsof -ti:5000 | xargs kill -9
```

Or change port in `backend/app.py` line 136.

## System Requirements

- Python 3.8 or higher
- 2GB free disk space (for ML libraries)
- 4GB RAM minimum
- Internet connection for installation

## Quick Test (Without Dependencies)

To test the code structure:

```bash
cd /home/tony/code/FitMentor/backend
python3 test_without_ml.py
```

This verifies the app structure is correct without requiring ML packages.
