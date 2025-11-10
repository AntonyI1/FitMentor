from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys

# Add backend directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.calorie_calculator import CalorieCalculator
from models.workout_suggester import WorkoutSuggester

app = Flask(__name__)
CORS(app)

# Initialize ML models
calorie_calculator = CalorieCalculator()
workout_suggester = WorkoutSuggester()

@app.route('/')
def home():
    return jsonify({
        'message': 'FitMentor AI API',
        'version': '1.0.0',
        'endpoints': {
            'calorie_calculator': '/api/calculate-calories',
            'workout_suggester': '/api/suggest-workout'
        }
    })

@app.route('/api/calculate-calories', methods=['POST'])
def calculate_calories():
    """
    Calculate maintenance calories and macronutrient breakdown
    Expected input:
    {
        "age": int,
        "height": float (cm),
        "weight": float (kg),
        "gender": str ("male" or "female"),
        "activity_level": str ("sedentary", "light", "moderate", "active", "very_active"),
        "goal": str ("lose", "maintain", "gain")
    }
    """
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ['age', 'height', 'weight', 'gender', 'activity_level', 'goal']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        # Calculate calories and macros
        result = calorie_calculator.calculate(
            age=data['age'],
            height=data['height'],
            weight=data['weight'],
            gender=data['gender'],
            activity_level=data['activity_level'],
            goal=data['goal']
        )

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/suggest-workout', methods=['POST'])
def suggest_workout():
    """
    Generate personalized workout plan
    Expected input:
    {
        "goal": str ("strength", "hypertrophy", "endurance", "weight_loss"),
        "experience": str ("beginner", "intermediate", "advanced"),
        "equipment": list of str (["barbell", "dumbbell", "machine", etc.]),
        "days_per_week": int (3-6),
        "session_duration": int (minutes, 30-120)
    }
    """
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ['goal', 'experience', 'equipment', 'days_per_week']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        # Generate workout plan
        result = workout_suggester.generate_plan(
            goal=data['goal'],
            experience=data['experience'],
            equipment=data['equipment'],
            days_per_week=data['days_per_week'],
            session_duration=data.get('session_duration', 60)
        )

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/exercises', methods=['GET'])
def get_exercises():
    """Get list of all available exercises with details"""
    try:
        exercises = workout_suggester.get_exercise_database()
        return jsonify(exercises)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Starting FitMentor API server...")
    print("Initializing ML models...")
    app.run(debug=True, host='0.0.0.0', port=5000)
