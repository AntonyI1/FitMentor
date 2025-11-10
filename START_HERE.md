# FitMentor - Quick Start Guide

## Getting Started

### Step 1: Install Dependencies

```bash
# Create a virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

### Step 2: Start the Backend Server

```bash
# Navigate to backend directory
cd backend

# Run the Flask API server
python app.py
```

The server will start on `http://localhost:5000`

You should see:
```
Starting FitMentor API server...
Initializing ML models...
 * Running on http://0.0.0.0:5000
```

### Step 3: Open the Frontend

Open `frontend/index.html` in your web browser. You can either:

1. Double-click the file in your file manager
2. Use a local development server (recommended):

```bash
# Using Python's built-in server
cd frontend
python -m http.server 8000

# Then open http://localhost:8000 in your browser
```

### Step 4: Test the Application

#### Test the Calorie Calculator:
1. Navigate to the "Calorie Calculator" section
2. Fill in your personal information:
   - Age, gender, height, weight
   - Activity level
   - Fitness goal
3. Click "Calculate"
4. View your personalized calorie and macro targets

#### Test the Workout Planner:
1. Navigate to the "AI Workout Planner" section
2. Select your training preferences:
   - Training goal (strength, hypertrophy, etc.)
   - Experience level
   - Days per week
   - Available equipment
3. Click "Generate Workout Plan"
4. View your personalized workout split and exercises

### Step 5: Run API Tests (Optional)

To verify all API endpoints are working:

```bash
cd backend/utils
python test_api.py
```

## Features Overview

### 1. Calorie Calculator
- **AI-Powered**: Uses TensorFlow neural network for BMR prediction
- **Accurate Formulas**: Validates with Mifflin-St Jeor equation
- **Smart Macros**: Goal-based macronutrient optimization
- **Personalized**: Adapts to your activity level and goals

### 2. Workout Suggester
- **Intelligent Exercise Selection**: PyTorch model for optimal exercise matching
- **Volume Optimization**: TensorFlow model for training volume
- **30+ Exercises**: Comprehensive exercise database
- **Multiple Splits**: 3-6 day programs (Full Body, Upper/Lower, PPL)
- **Progression Plans**: Clear strategies for continuous improvement

## Troubleshooting

### Backend Server Issues

**Error: "Module not found"**
- Make sure you've installed all dependencies: `pip install -r requirements.txt`
- Check that your virtual environment is activated

**Error: "Port already in use"**
- Another application is using port 5000
- Stop the other application or change the port in `backend/app.py`

**TensorFlow/PyTorch Installation Issues**
- These libraries can be large and complex
- For CPU-only versions:
  ```bash
  pip install tensorflow-cpu
  pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
  ```

### Frontend Issues

**Error: "Failed to fetch" or "Network Error"**
- Ensure the backend server is running
- Check that the API URL in `frontend/js/app.js` matches your server
- Try opening the browser console (F12) to see detailed errors

**Styles Not Loading**
- Make sure you're accessing via a web server, not just file://
- Use `python -m http.server` as shown above

### Browser Compatibility

Recommended browsers:
- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Project Structure

```
FitMentor/
├── backend/
│   ├── app.py                          # Flask API server
│   ├── models/
│   │   ├── calorie_calculator.py       # TensorFlow calorie model
│   │   └── workout_suggester.py        # PyTorch workout model
│   └── utils/
│       └── test_api.py                 # API test suite
├── frontend/
│   ├── index.html                      # Main UI
│   ├── css/
│   │   └── styles.css                  # Responsive styling
│   └── js/
│       └── app.js                      # API integration
├── requirements.txt                     # Python dependencies
└── README.md                           # Project documentation
```

## Next Steps

1. **Train Custom Models**: Replace synthetic data with real user data
2. **Add Exercise Images**: Populate `frontend/images/exercises/` with exercise photos
3. **Expand Exercise Database**: Add more exercises to `workout_suggester.py`
4. **Add User Accounts**: Implement authentication and save user progress
5. **Mobile App**: Build native mobile versions

## Need Help?

- Check the README.md for detailed documentation
- Review the code comments for implementation details
- Test the API using `backend/utils/test_api.py`

## Development Notes

- Backend runs on: http://localhost:5000
- Frontend runs on: http://localhost:8000 (or just open index.html)
- All commits are made under user: Antonyi1
- Models auto-train on first run using synthetic data

---

**Ready to start your fitness journey with AI? Let's go!**
