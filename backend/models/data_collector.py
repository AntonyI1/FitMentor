import json
import os
from datetime import datetime

class DataCollector:
    """
    Collects user inputs and results for future model training
    Helps improve ML models over time with real data
    """

    def __init__(self, data_dir='../data'):
        self.data_dir = os.path.join(os.path.dirname(__file__), data_dir)
        os.makedirs(self.data_dir, exist_ok=True)

        self.calorie_data_file = os.path.join(self.data_dir, 'calorie_calculations.jsonl')
        self.workout_data_file = os.path.join(self.data_dir, 'workout_plans.jsonl')

    def save_calorie_calculation(self, input_data, result):
        """Save calorie calculation for future training"""
        record = {
            'timestamp': datetime.now().isoformat(),
            'input': input_data,
            'output': result
        }

        with open(self.calorie_data_file, 'a') as f:
            f.write(json.dumps(record) + '\n')

    def save_workout_plan(self, input_data, result):
        """Save workout plan generation for future training"""
        record = {
            'timestamp': datetime.now().isoformat(),
            'input': input_data,
            'output': result
        }

        with open(self.workout_data_file, 'a') as f:
            f.write(json.dumps(record) + '\n')

    def get_calorie_data_count(self):
        """Get number of calorie calculations collected"""
        if not os.path.exists(self.calorie_data_file):
            return 0

        with open(self.calorie_data_file, 'r') as f:
            return sum(1 for _ in f)

    def get_workout_data_count(self):
        """Get number of workout plans collected"""
        if not os.path.exists(self.workout_data_file):
            return 0

        with open(self.workout_data_file, 'r') as f:
            return sum(1 for _ in f)

    def load_calorie_data(self):
        """Load all calorie calculation data for training"""
        if not os.path.exists(self.calorie_data_file):
            return []

        data = []
        with open(self.calorie_data_file, 'r') as f:
            for line in f:
                data.append(json.loads(line))
        return data

    def load_workout_data(self):
        """Load all workout plan data for training"""
        if not os.path.exists(self.workout_data_file):
            return []

        data = []
        with open(self.workout_data_file, 'r') as f:
            for line in f:
                data.append(json.loads(line))
        return data
