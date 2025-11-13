from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys

# Add backend directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.calorie_calculator import CalorieCalculator
from models.workout_suggester import WorkoutSuggester
from models.data_collector import DataCollector

app = Flask(__name__)
CORS(app)

# Initialize ML models and data collector
calorie_calculator = CalorieCalculator()
workout_suggester = WorkoutSuggester()
data_collector = DataCollector()

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
    """Calculate maintenance calories and macronutrient breakdown"""
    try:
        data = request.get_json()

        required_fields = ['age', 'height', 'weight', 'gender', 'activity_level', 'goal']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        result = calorie_calculator.calculate(
            age=data['age'],
            height=data['height'],
            weight=data['weight'],
            gender=data['gender'],
            activity_level=data['activity_level'],
            goal=data['goal']
        )

        # Save data for future model improvement (temporarily disabled)
        # data_collector.save_calorie_calculation(data, result)

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/suggest-workout', methods=['POST'])
def suggest_workout():
    """Generate personalized workout plan"""
    try:
        data = request.get_json()

        required_fields = ['gender', 'goal', 'experience', 'equipment', 'days_per_week']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        result = workout_suggester.generate_plan(
            goal=data['goal'],
            experience=data['experience'],
            equipment=data['equipment'],
            days_per_week=data['days_per_week'],
            session_duration=data.get('session_duration', 60),
            gender=data['gender']
        )

        data_collector.save_workout_plan(data, result)

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

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get statistics about collected data for model improvement"""
    try:
        return jsonify({
            'calorie_calculations': data_collector.get_calorie_data_count(),
            'workout_plans': data_collector.get_workout_data_count(),
            'message': 'Data collected for continuous model improvement'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Starting FitMentor API server...")
    print("Initializing ML models...")
    app.run(debug=True, host='0.0.0.0', port=5000)
