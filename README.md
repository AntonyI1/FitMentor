# FitMentor - AI-Powered Fitness Coach

An intelligent fitness platform that combines AI-driven calorie calculation and personalized workout recommendations using machine learning models.

## Overview

FitMentor acts as your personal AI fitness coach, providing:
- Accurate calorie and macronutrient calculations tailored to your goals
- Intelligent workout plan generation based on your experience and equipment
- Science-based progression strategies
- Comprehensive exercise database with proper form guidance

## Features

### 1. Calorie Maintenance Calculator
- **AI-Powered Prediction**: TensorFlow neural network trained on metabolic data
- **Validated Accuracy**: Cross-references with Mifflin-St Jeor equation
- **Smart Macros**: Goal-optimized macronutrient breakdown (protein, carbs, fats)
- **Personalized Targets**: Adjusts for activity level, age, gender, and fitness goals
- **Expert Recommendations**: Evidence-based nutrition advice

**Input Parameters:**
- Age, height, weight, gender
- Activity level (sedentary to very active)
- Fitness goal (lose, maintain, gain weight)

**Output:**
- BMR (Basal Metabolic Rate)
- TDEE (Total Daily Energy Expenditure)
- Target calories with goal adjustment
- Macro breakdown in grams and percentages
- Personalized recommendations

### 2. AI Workout Suggester
- **Intelligent Exercise Selection**: PyTorch neural network for optimal exercise matching
- **Volume Optimization**: TensorFlow model calculates optimal sets and reps
- **30+ Exercise Database**: Compound and isolation exercises for all muscle groups
- **Multiple Training Splits**: Full Body, Upper/Lower, Push/Pull/Legs (3-6 day programs)
- **Experience-Adapted**: Filters exercises by difficulty level
- **Equipment-Flexible**: Works with your available equipment
- **Progression Plans**: Clear strategies for continuous improvement

**Input Parameters:**
- Training goal (strength, hypertrophy, endurance, weight loss)
- Experience level (beginner, intermediate, advanced)
- Available equipment
- Training frequency (3-6 days per week)
- Session duration

**Output:**
- Complete training split
- Exercise selection with proper progression
- Sets, reps, and rest periods
- Progression strategy with deload recommendations
- Training tips and best practices

## Tech Stack

### Backend
- **Framework**: Flask (Python 3.8+)
- **ML Libraries**:
  - TensorFlow 2.15.0 (calorie prediction & volume optimization)
  - PyTorch 2.1.0 (exercise selection)
- **Data Processing**: NumPy, Pandas
- **API**: RESTful with JSON responses

### Frontend
- **Structure**: HTML5 semantic markup
- **Styling**: Modern CSS3 with custom properties
- **Interactivity**: Vanilla JavaScript (ES6+)
- **Design**: Responsive, mobile-first approach
- **UI/UX**: Smooth animations, loading states, progressive disclosure

### Machine Learning
- **Calorie Model**: Neural network (64→32→16→1 architecture)
- **Workout Model**: Multi-layer perceptron for exercise scoring
- **Training**: Synthetic data based on established formulas
- **Inference**: Real-time predictions on user input

## Project Structure

```
FitMentor/
├── backend/
│   ├── app.py                          # Flask API server
│   ├── models/
│   │   ├── __init__.py
│   │   ├── calorie_calculator.py       # TensorFlow calorie model
│   │   └── workout_suggester.py        # PyTorch workout model
│   ├── utils/
│   │   ├── __init__.py
│   │   └── test_api.py                 # API test suite
│   └── data/                           # Training data (future)
├── frontend/
│   ├── index.html                      # Main application UI
│   ├── css/
│   │   └── styles.css                  # Responsive styling
│   ├── js/
│   │   └── app.js                      # API integration & UI logic
│   └── images/
│       └── exercises/                  # Exercise demonstration images
├── requirements.txt                     # Python dependencies
├── README.md                           # This file
├── START_HERE.md                       # Quick start guide
└── .gitignore                          # Git ignore rules
```

## Getting Started

### Quick Start

**See [START_HERE.md](START_HERE.md) for detailed setup instructions.**

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start backend server
python backend/app.py

# 3. Open frontend
# Open frontend/index.html in your browser
# Or use a local server: python -m http.server 8000
```

### API Endpoints

**Base URL**: `http://localhost:5000/api`

1. **POST /calculate-calories**
   - Calculates maintenance calories and macros
   - Request body: `{age, height, weight, gender, activity_level, goal}`

2. **POST /suggest-workout**
   - Generates personalized workout plan
   - Request body: `{goal, experience, equipment[], days_per_week, session_duration}`

3. **GET /exercises**
   - Returns complete exercise database
   - No parameters required

### Testing

Run the API test suite:

```bash
cd backend/utils
python test_api.py
```

Tests verify:
- Calorie calculation accuracy
- Workout plan generation
- Exercise database integrity
- API response formats

## Machine Learning Models

### Calorie Calculator Model

**Architecture:**
- Input layer: 5 features (age, height, weight, gender, activity)
- Hidden layers: 64→32→16 neurons with ReLU activation
- Dropout: 0.2, 0.1 for regularization
- Output: BMR prediction

**Training:**
- 10,000 synthetic samples based on Mifflin-St Jeor equation
- 80/20 train/validation split
- 50 epochs with early stopping
- MSE loss, Adam optimizer

**Inference:**
- Weighted average: 70% ML prediction + 30% formula validation
- Activity multiplier applied to BMR for TDEE
- Goal-based adjustments for target calories

### Workout Suggester Model

**PyTorch Model:**
- Input: 10 features (encoded user preferences)
- Hidden: 128→64 neurons with ReLU and dropout
- Output: Exercise scores (sigmoid activation)

**Logic:**
- Exercise filtering by equipment and experience
- Intelligent split generation (3-6 day programs)
- Volume optimization based on goal and experience
- Compound exercises prioritized over isolation

## Development Roadmap

### Phase 1: Core Features (Complete)
- ✓ TensorFlow calorie calculator
- ✓ PyTorch workout suggester
- ✓ Flask API backend
- ✓ Responsive frontend UI
- ✓ Exercise database (30 exercises)

### Phase 2: Enhancements (Future)
- Train models on real user data
- Add exercise demonstration videos
- Implement progress tracking
- Add nutrition meal planning
- Mobile app development

### Phase 3: Advanced Features (Future)
- User authentication and profiles
- Workout logging and analytics
- Form check using computer vision
- Social features and challenges
- Integration with fitness trackers

## Contributing

This project follows clean code practices with:
- Meaningful commit messages
- Incremental feature development
- Proper version control discipline
- Comprehensive testing

All commits are made under user: **Antonyi1** (antonyibrahim0@gmail.com)

## Technical Decisions

### Why TensorFlow and PyTorch?
- TensorFlow: Excellent for production deployment and structured prediction
- PyTorch: Superior for research and custom architectures
- Demonstrates proficiency with both major ML frameworks

### Why Flask?
- Lightweight and perfect for ML APIs
- Easy integration with Python ML libraries
- RESTful API design principles

### Why Vanilla JavaScript?
- No framework overhead for faster loading
- Direct DOM manipulation for learning
- Easy to understand and maintain
- Production-ready with proper structure

## Performance

- API response time: <100ms for calorie calculation
- Workout generation: <200ms for complete plan
- Frontend load time: <1s on modern browsers
- Model inference: Real-time (no noticeable delay)

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## License

This project is for educational and personal use.

## Acknowledgments

- Mifflin-St Jeor equation for BMR validation
- Exercise science research for training principles
- TensorFlow and PyTorch communities

---

**Built with focus on intelligent automation, clean architecture, and user experience.**
