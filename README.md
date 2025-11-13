# FitMentor - AI Fitness Coach

An intelligent fitness platform that provides AI-driven calorie calculations and personalized workout recommendations using machine learning.

## Features

### Calorie Calculator
- **AI-Powered Prediction**: TensorFlow neural network for accurate BMR/TDEE calculation
- **Smart Macros**: Goal-optimized macronutrient breakdown
- **Personalized**: Adjusts for activity level, age, gender, and fitness goals

### Workout Planner
- **Intelligent Exercise Selection**: PyTorch model for optimal exercise matching
- **30+ Exercise Database**: Compound and isolation exercises for all muscle groups
- **Multiple Training Splits**: Full Body, Upper/Lower, Push/Pull/Legs (3-6 day programs)
- **Experience-Adapted**: Filters exercises by difficulty level and available equipment

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Start Backend

```bash
./start_backend.sh
# Or manually: python backend/app.py
```

Server runs on `http://localhost:5000`

### 3. Start Frontend

```bash
./start_frontend.sh
# Or manually: python -m http.server 8000 in frontend/
```

Open `http://localhost:8000` in your browser

## Tech Stack

**Backend:**
- Flask (Python 3.8+)
- TensorFlow 2.15.0 (calorie prediction)
- PyTorch 2.1.0 (exercise selection)
- NumPy, Pandas

**Frontend:**
- HTML5, CSS3, Vanilla JavaScript
- Responsive, mobile-first design

**ML Models:**
- Calorie Model: Neural network (64→32→16→1)
- Workout Model: Multi-layer perceptron for exercise scoring

## API Endpoints

Base URL: `http://localhost:5000/api`

- **POST /calculate-calories** - Calculate maintenance calories and macros
- **POST /suggest-workout** - Generate personalized workout plan
- **GET /exercises** - Get complete exercise database
- **GET /stats** - View data collection statistics

## Project Structure

```
FitMentor/
├── backend/
│   ├── app.py                    # Flask API server
│   ├── models/
│   │   ├── calorie_calculator.py # TensorFlow model
│   │   ├── workout_suggester.py  # PyTorch model
│   │   └── data_collector.py     # Data collection
│   └── utils/
│       └── test_api.py           # API tests
├── frontend/
│   ├── index.html                # Main UI
│   ├── css/styles.css            # Styling
│   ├── js/app.js                 # Frontend logic
│   └── images/exercises/         # Exercise images
├── requirements.txt
└── README.md
```

## Development

Run API tests:
```bash
cd backend/utils
python test_api.py
```

## License

Educational and personal use.
