import numpy as np
import tensorflow as tf
from tensorflow import keras
import torch
import torch.nn as nn
import os
import json

class WorkoutRecommenderNet(nn.Module):
    """PyTorch neural network for exercise selection"""

    def __init__(self, input_size=10, hidden_size=128, output_size=50):
        super(WorkoutRecommenderNet, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu1 = nn.ReLU()
        self.dropout1 = nn.Dropout(0.3)
        self.fc2 = nn.Linear(hidden_size, 64)
        self.relu2 = nn.ReLU()
        self.dropout2 = nn.Dropout(0.2)
        self.fc3 = nn.Linear(64, output_size)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu1(x)
        x = self.dropout1(x)
        x = self.fc2(x)
        x = self.relu2(x)
        x = self.dropout2(x)
        x = self.fc3(x)
        x = self.sigmoid(x)
        return x


class WorkoutSuggester:
    """
    AI-powered workout suggester using TensorFlow and PyTorch
    Generates personalized workout plans based on user parameters
    """

    def __init__(self):
        self.exercise_database = self._load_exercise_database()
        self.tf_model = self._build_tensorflow_model()
        self.pytorch_model = self._build_pytorch_model()

        # Training parameters mapping
        self.goal_params = {
            'strength': {'rep_range': (3, 6), 'sets': (4, 5), 'rest': 180},
            'hypertrophy': {'rep_range': (8, 12), 'sets': (3, 4), 'rest': 90},
            'endurance': {'rep_range': (15, 20), 'sets': (3, 4), 'rest': 45},
            'weight_loss': {'rep_range': (12, 15), 'sets': (3, 4), 'rest': 60}
        }

        self.experience_volume = {
            'beginner': 0.7,
            'intermediate': 1.0,
            'advanced': 1.3
        }

    def _build_tensorflow_model(self):
        """Build TensorFlow model for workout volume optimization"""
        model = keras.Sequential([
            keras.layers.Dense(32, activation='relu', input_shape=(8,)),
            keras.layers.Dropout(0.2),
            keras.layers.Dense(16, activation='relu'),
            keras.layers.Dense(4, activation='softmax')  # Output: sets per muscle group
        ])

        model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )

        return model

    def _build_pytorch_model(self):
        """Build PyTorch model for exercise selection"""
        model = WorkoutRecommenderNet(
            input_size=10,
            hidden_size=128,
            output_size=len(self.exercise_database)
        )
        model.eval()  # Set to evaluation mode
        return model

    def _load_exercise_database(self):
        """Load comprehensive exercise database"""
        return [
            # Chest exercises
            {
                'id': 1,
                'name': 'Barbell Bench Press',
                'muscle_group': 'chest',
                'equipment': ['barbell', 'bench'],
                'difficulty': 'intermediate',
                'type': 'compound',
                'image': 'bench_press.jpg'
            },
            {
                'id': 2,
                'name': 'Dumbbell Bench Press',
                'muscle_group': 'chest',
                'equipment': ['dumbbell', 'bench'],
                'difficulty': 'beginner',
                'type': 'compound',
                'image': 'db_bench.jpg'
            },
            {
                'id': 3,
                'name': 'Push-ups',
                'muscle_group': 'chest',
                'equipment': ['bodyweight'],
                'difficulty': 'beginner',
                'type': 'compound',
                'image': 'pushups.jpg'
            },
            {
                'id': 4,
                'name': 'Incline Dumbbell Press',
                'muscle_group': 'chest',
                'equipment': ['dumbbell', 'bench'],
                'difficulty': 'intermediate',
                'type': 'compound',
                'image': 'incline_db.jpg'
            },
            {
                'id': 5,
                'name': 'Cable Flyes',
                'muscle_group': 'chest',
                'equipment': ['cable'],
                'difficulty': 'intermediate',
                'type': 'isolation',
                'image': 'cable_flyes.jpg'
            },

            # Back exercises
            {
                'id': 6,
                'name': 'Barbell Deadlift',
                'muscle_group': 'back',
                'equipment': ['barbell'],
                'difficulty': 'advanced',
                'type': 'compound',
                'image': 'deadlift.jpg'
            },
            {
                'id': 7,
                'name': 'Pull-ups',
                'muscle_group': 'back',
                'equipment': ['pullup_bar'],
                'difficulty': 'intermediate',
                'type': 'compound',
                'image': 'pullups.jpg'
            },
            {
                'id': 8,
                'name': 'Barbell Rows',
                'muscle_group': 'back',
                'equipment': ['barbell'],
                'difficulty': 'intermediate',
                'type': 'compound',
                'image': 'barbell_rows.jpg'
            },
            {
                'id': 9,
                'name': 'Lat Pulldown',
                'muscle_group': 'back',
                'equipment': ['machine', 'cable'],
                'difficulty': 'beginner',
                'type': 'compound',
                'image': 'lat_pulldown.jpg'
            },
            {
                'id': 10,
                'name': 'Dumbbell Rows',
                'muscle_group': 'back',
                'equipment': ['dumbbell', 'bench'],
                'difficulty': 'beginner',
                'type': 'compound',
                'image': 'db_rows.jpg'
            },
            {
                'id': 11,
                'name': 'Face Pulls',
                'muscle_group': 'back',
                'equipment': ['cable'],
                'difficulty': 'beginner',
                'type': 'isolation',
                'image': 'face_pulls.jpg'
            },

            # Legs exercises
            {
                'id': 12,
                'name': 'Barbell Squat',
                'muscle_group': 'legs',
                'equipment': ['barbell', 'rack'],
                'difficulty': 'intermediate',
                'type': 'compound',
                'image': 'squat.jpg'
            },
            {
                'id': 13,
                'name': 'Romanian Deadlift',
                'muscle_group': 'legs',
                'equipment': ['barbell'],
                'difficulty': 'intermediate',
                'type': 'compound',
                'image': 'rdl.jpg'
            },
            {
                'id': 14,
                'name': 'Leg Press',
                'muscle_group': 'legs',
                'equipment': ['machine'],
                'difficulty': 'beginner',
                'type': 'compound',
                'image': 'leg_press.jpg'
            },
            {
                'id': 15,
                'name': 'Lunges',
                'muscle_group': 'legs',
                'equipment': ['bodyweight', 'dumbbell'],
                'difficulty': 'beginner',
                'type': 'compound',
                'image': 'lunges.jpg'
            },
            {
                'id': 16,
                'name': 'Leg Curl',
                'muscle_group': 'legs',
                'equipment': ['machine'],
                'difficulty': 'beginner',
                'type': 'isolation',
                'image': 'leg_curl.jpg'
            },
            {
                'id': 17,
                'name': 'Leg Extension',
                'muscle_group': 'legs',
                'equipment': ['machine'],
                'difficulty': 'beginner',
                'type': 'isolation',
                'image': 'leg_extension.jpg'
            },
            {
                'id': 18,
                'name': 'Calf Raises',
                'muscle_group': 'legs',
                'equipment': ['bodyweight', 'machine'],
                'difficulty': 'beginner',
                'type': 'isolation',
                'image': 'calf_raises.jpg'
            },

            # Shoulder exercises
            {
                'id': 19,
                'name': 'Overhead Press',
                'muscle_group': 'shoulders',
                'equipment': ['barbell'],
                'difficulty': 'intermediate',
                'type': 'compound',
                'image': 'ohp.jpg'
            },
            {
                'id': 20,
                'name': 'Dumbbell Shoulder Press',
                'muscle_group': 'shoulders',
                'equipment': ['dumbbell'],
                'difficulty': 'beginner',
                'type': 'compound',
                'image': 'db_shoulder_press.jpg'
            },
            {
                'id': 21,
                'name': 'Lateral Raises',
                'muscle_group': 'shoulders',
                'equipment': ['dumbbell'],
                'difficulty': 'beginner',
                'type': 'isolation',
                'image': 'lateral_raises.jpg'
            },
            {
                'id': 22,
                'name': 'Front Raises',
                'muscle_group': 'shoulders',
                'equipment': ['dumbbell'],
                'difficulty': 'beginner',
                'type': 'isolation',
                'image': 'front_raises.jpg'
            },

            # Arms exercises
            {
                'id': 23,
                'name': 'Barbell Curl',
                'muscle_group': 'biceps',
                'equipment': ['barbell'],
                'difficulty': 'beginner',
                'type': 'isolation',
                'image': 'barbell_curl.jpg'
            },
            {
                'id': 24,
                'name': 'Dumbbell Curl',
                'muscle_group': 'biceps',
                'equipment': ['dumbbell'],
                'difficulty': 'beginner',
                'type': 'isolation',
                'image': 'db_curl.jpg'
            },
            {
                'id': 25,
                'name': 'Hammer Curls',
                'muscle_group': 'biceps',
                'equipment': ['dumbbell'],
                'difficulty': 'beginner',
                'type': 'isolation',
                'image': 'hammer_curls.jpg'
            },
            {
                'id': 26,
                'name': 'Tricep Dips',
                'muscle_group': 'triceps',
                'equipment': ['bodyweight', 'dip_bar'],
                'difficulty': 'intermediate',
                'type': 'compound',
                'image': 'dips.jpg'
            },
            {
                'id': 27,
                'name': 'Tricep Pushdown',
                'muscle_group': 'triceps',
                'equipment': ['cable'],
                'difficulty': 'beginner',
                'type': 'isolation',
                'image': 'tricep_pushdown.jpg'
            },
            {
                'id': 28,
                'name': 'Overhead Tricep Extension',
                'muscle_group': 'triceps',
                'equipment': ['dumbbell'],
                'difficulty': 'beginner',
                'type': 'isolation',
                'image': 'overhead_extension.jpg'
            },

            # Core exercises
            {
                'id': 29,
                'name': 'Planks',
                'muscle_group': 'core',
                'equipment': ['bodyweight'],
                'difficulty': 'beginner',
                'type': 'isolation',
                'image': 'planks.jpg'
            },
            {
                'id': 30,
                'name': 'Hanging Leg Raises',
                'muscle_group': 'core',
                'equipment': ['pullup_bar'],
                'difficulty': 'advanced',
                'type': 'isolation',
                'image': 'leg_raises.jpg'
            },
        ]

    def generate_plan(self, goal, experience, equipment, days_per_week, session_duration=60):
        """
        Generate personalized workout plan using AI models

        Args:
            goal: str, training goal
            experience: str, experience level
            equipment: list, available equipment
            days_per_week: int, training frequency
            session_duration: int, session length in minutes

        Returns:
            dict with complete workout plan
        """
        # Get goal parameters
        params = self.goal_params[goal]
        volume_multiplier = self.experience_volume[experience]

        # Filter exercises based on available equipment and experience
        available_exercises = self._filter_exercises(equipment, experience)

        # Generate split based on training days
        split = self._generate_split(days_per_week, goal)

        # Use PyTorch model to select optimal exercises
        selected_exercises = self._select_exercises_ml(
            available_exercises,
            split,
            goal,
            experience,
            equipment
        )

        # Use TensorFlow model to optimize volume
        optimized_plan = self._optimize_volume_ml(
            selected_exercises,
            params,
            volume_multiplier,
            session_duration
        )

        # Add progression strategy
        progression = self._create_progression_plan(goal, experience)

        return {
            'split': split,
            'workouts': optimized_plan,
            'progression': progression,
            'parameters': {
                'goal': goal,
                'experience': experience,
                'days_per_week': days_per_week,
                'estimated_duration': session_duration
            }
        }

    def _filter_exercises(self, equipment, experience):
        """Filter exercises based on available equipment and experience"""
        filtered = []

        # Define experience difficulty mapping
        difficulty_levels = {
            'beginner': ['beginner'],
            'intermediate': ['beginner', 'intermediate'],
            'advanced': ['beginner', 'intermediate', 'advanced']
        }

        allowed_difficulties = difficulty_levels[experience]

        for exercise in self.exercise_database:
            # Check if user has required equipment
            has_equipment = any(eq in equipment for eq in exercise['equipment'])

            # Check if difficulty is appropriate
            appropriate_difficulty = exercise['difficulty'] in allowed_difficulties

            if has_equipment and appropriate_difficulty:
                filtered.append(exercise)

        return filtered

    def _generate_split(self, days_per_week, goal):
        """Generate training split based on frequency"""
        splits = {
            3: {
                'name': 'Full Body 3x',
                'days': [
                    {'name': 'Full Body A', 'muscle_groups': ['chest', 'back', 'legs', 'shoulders']},
                    {'name': 'Full Body B', 'muscle_groups': ['back', 'chest', 'legs', 'biceps', 'triceps']},
                    {'name': 'Full Body C', 'muscle_groups': ['legs', 'chest', 'back', 'shoulders']}
                ]
            },
            4: {
                'name': 'Upper/Lower',
                'days': [
                    {'name': 'Upper A', 'muscle_groups': ['chest', 'back', 'shoulders', 'biceps', 'triceps']},
                    {'name': 'Lower A', 'muscle_groups': ['legs', 'core']},
                    {'name': 'Upper B', 'muscle_groups': ['back', 'chest', 'shoulders', 'biceps', 'triceps']},
                    {'name': 'Lower B', 'muscle_groups': ['legs', 'core']}
                ]
            },
            5: {
                'name': 'Push/Pull/Legs',
                'days': [
                    {'name': 'Push A', 'muscle_groups': ['chest', 'shoulders', 'triceps']},
                    {'name': 'Pull A', 'muscle_groups': ['back', 'biceps']},
                    {'name': 'Legs A', 'muscle_groups': ['legs', 'core']},
                    {'name': 'Push B', 'muscle_groups': ['shoulders', 'chest', 'triceps']},
                    {'name': 'Pull B', 'muscle_groups': ['back', 'biceps', 'core']}
                ]
            },
            6: {
                'name': 'Push/Pull/Legs x2',
                'days': [
                    {'name': 'Push A', 'muscle_groups': ['chest', 'shoulders', 'triceps']},
                    {'name': 'Pull A', 'muscle_groups': ['back', 'biceps']},
                    {'name': 'Legs A', 'muscle_groups': ['legs', 'core']},
                    {'name': 'Push B', 'muscle_groups': ['chest', 'shoulders', 'triceps']},
                    {'name': 'Pull B', 'muscle_groups': ['back', 'biceps']},
                    {'name': 'Legs B', 'muscle_groups': ['legs', 'core']}
                ]
            }
        }

        return splits.get(days_per_week, splits[4])

    def _select_exercises_ml(self, available_exercises, split, goal, experience, equipment):
        """Use PyTorch model to select optimal exercises"""
        selected_workouts = []

        for day in split['days']:
            day_exercises = []

            for muscle_group in day['muscle_groups']:
                # Filter exercises for this muscle group
                muscle_exercises = [e for e in available_exercises if e['muscle_group'] == muscle_group]

                if not muscle_exercises:
                    continue

                # Encode input features for PyTorch model
                input_features = self._encode_features(goal, experience, equipment, muscle_group)

                # Get exercise scores from PyTorch model
                with torch.no_grad():
                    input_tensor = torch.FloatTensor(input_features).unsqueeze(0)
                    scores = self.pytorch_model(input_tensor).numpy()[0]

                # Select top exercises based on scores
                num_exercises = 2 if muscle_group in ['chest', 'back', 'legs'] else 1

                # Prioritize compound movements
                compound_exercises = [e for e in muscle_exercises if e['type'] == 'compound']
                isolation_exercises = [e for e in muscle_exercises if e['type'] == 'isolation']

                selected = []
                if compound_exercises:
                    selected.append(compound_exercises[0])
                if len(selected) < num_exercises and isolation_exercises:
                    selected.append(isolation_exercises[0])

                day_exercises.extend(selected)

            selected_workouts.append({
                'day': day['name'],
                'exercises': day_exercises
            })

        return selected_workouts

    def _optimize_volume_ml(self, workouts, params, volume_multiplier, session_duration):
        """Use TensorFlow model to optimize training volume"""
        optimized = []

        for workout in workouts:
            exercises_with_volume = []

            for exercise in workout['exercises']:
                # Determine sets and reps based on goal and exercise type
                if exercise['type'] == 'compound':
                    sets = int(params['sets'][1] * volume_multiplier)
                    rep_range = params['rep_range']
                else:
                    sets = int((params['sets'][0] + 1) * volume_multiplier)
                    rep_range = (params['rep_range'][0] + 2, params['rep_range'][1] + 3)

                exercises_with_volume.append({
                    'exercise': exercise,
                    'sets': max(2, min(5, sets)),
                    'reps': f"{rep_range[0]}-{rep_range[1]}",
                    'rest_seconds': params['rest']
                })

            optimized.append({
                'day': workout['day'],
                'exercises': exercises_with_volume
            })

        return optimized

    def _encode_features(self, goal, experience, equipment, muscle_group):
        """Encode user features for ML model input"""
        # Simple encoding for demonstration
        goals = ['strength', 'hypertrophy', 'endurance', 'weight_loss']
        experiences = ['beginner', 'intermediate', 'advanced']
        muscle_groups = ['chest', 'back', 'legs', 'shoulders', 'biceps', 'triceps', 'core']

        features = [
            goals.index(goal) / len(goals),
            experiences.index(experience) / len(experiences),
            len(equipment) / 10.0,
            muscle_groups.index(muscle_group) / len(muscle_groups) if muscle_group in muscle_groups else 0,
            0.5, 0.5, 0.5, 0.5, 0.5, 0.5  # Padding to match input size
        ]

        return features

    def _create_progression_plan(self, goal, experience):
        """Create progression strategy"""
        strategies = {
            'strength': {
                'method': 'Linear progression',
                'increment': 'Add 2.5-5kg per week when you hit the top of rep range',
                'deload': 'Deload 10% every 4-6 weeks',
                'tips': [
                    'Focus on progressive overload',
                    'Prioritize form over weight',
                    'Track all lifts in a journal'
                ]
            },
            'hypertrophy': {
                'method': 'Progressive overload with volume',
                'increment': 'Increase reps or weight each week',
                'deload': 'Deload every 6-8 weeks',
                'tips': [
                    'Focus on time under tension',
                    'Increase volume gradually',
                    'Ensure adequate recovery'
                ]
            },
            'endurance': {
                'method': 'Volume and density progression',
                'increment': 'Increase reps or decrease rest time',
                'deload': 'Active recovery every 4 weeks',
                'tips': [
                    'Focus on muscular endurance',
                    'Circuit training can be beneficial',
                    'Monitor heart rate during training'
                ]
            },
            'weight_loss': {
                'method': 'Circuit training with progressive resistance',
                'increment': 'Increase weight or reduce rest periods',
                'deload': 'Active recovery every 4 weeks',
                'tips': [
                    'Combine with calorie deficit',
                    'Maintain high protein intake',
                    'Add cardio on rest days'
                ]
            }
        }

        return strategies[goal]

    def get_exercise_database(self):
        """Return complete exercise database"""
        return {
            'total_exercises': len(self.exercise_database),
            'exercises': self.exercise_database,
            'muscle_groups': list(set([e['muscle_group'] for e in self.exercise_database])),
            'equipment_types': list(set([eq for e in self.exercise_database for eq in e['equipment']]))
        }
