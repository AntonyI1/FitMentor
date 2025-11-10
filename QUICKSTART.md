# Quick Start - Run FitMentor

## Step 1: Install Dependencies

```bash
cd /home/tony/code/FitMentor
./setup.sh
```

This will:
- Create a virtual environment
- Install TensorFlow, PyTorch, Flask, and all dependencies
- Takes 5-10 minutes depending on your internet speed

## Step 2: Start Backend Server

```bash
./run.sh
```

You should see:
```
Starting FitMentor API server...
Initializing ML models...
 * Running on http://0.0.0.0:5000
```

**Keep this terminal open!** The server needs to stay running.

## Step 3: Open Frontend

Open a new terminal and run:

```bash
cd /home/tony/code/FitMentor/frontend
python3 -m http.server 8000
```

Then open your browser to:
**http://localhost:8000**

Or you can just double-click `frontend/index.html` to open directly in your browser.

## Alternative: Manual Install

If setup.sh doesn't work:

```bash
# Install dependencies manually
cd /home/tony/code/FitMentor
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Start backend
cd backend
python3 app.py
```

## Testing

Once running, try:

1. **Calorie Calculator**: Fill in your info and click Calculate
2. **Workout Planner**: Select preferences and click Generate

## Troubleshooting

**"Module not found" errors**: Make sure virtual environment is activated
```bash
source venv/bin/activate
```

**Port already in use**: Change port in `backend/app.py` line 136
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Changed from 5000
```

**TensorFlow/PyTorch installation fails**: Try CPU-only versions
```bash
pip install tensorflow-cpu torch torchvision --index-url https://download.pytorch.org/whl/cpu
```
