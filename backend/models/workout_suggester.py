"""
Evidence-Based Workout Suggester
Principles: Proper exercise ordering, appropriate volume, and progression
"""

import numpy as np
import torch
import torch.nn as nn

# TODO: Train PyTorch model on real user data for exercise selection


class WorkoutRecommenderNet(nn.Module):
    """PyTorch neural network for exercise personalization"""

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
        x = self.dropout1(self.relu1(self.fc1(x)))
        x = self.dropout2(self.relu2(self.fc2(x)))
        return self.sigmoid(self.fc3(x))


class WorkoutSuggester:
    def __init__(self):
        self.exercise_database = self._load_exercise_database()
        self.pytorch_model = self._build_pytorch_model()

        self.goal_params = {
            'strength': {'rep_range': (3, 6), 'sets': 4, 'compound_rest': 180, 'isolation_rest': 120, 'rir': 1},
            'hypertrophy': {'rep_range': (8, 12), 'sets': 3, 'compound_rest': 120, 'isolation_rest': 60, 'rir': 1},
            'endurance': {'rep_range': (15, 20), 'sets': 3, 'compound_rest': 60, 'isolation_rest': 45, 'rir': 2},
            'weight_loss': {'rep_range': (12, 15), 'sets': 3, 'compound_rest': 60, 'isolation_rest': 45, 'rir': 1}
        }

        self.experience_volume = {'beginner': 0.85, 'intermediate': 1.0, 'advanced': 1.15}

    def _build_pytorch_model(self):
        model = WorkoutRecommenderNet(input_size=10, hidden_size=128,
                                     output_size=len(self.exercise_database) if hasattr(self, 'exercise_database') else 50)
        model.eval()
        return model

    def _load_exercise_database(self):
        return [
            # CHEST
            {'id': 1, 'name': 'Barbell Bench Press', 'muscle_group': 'chest', 'subcategory': 'mid_chest',
             'equipment': ['barbell', 'bench', 'rack'], 'difficulty': 'intermediate', 'type': 'compound',
             'category': 'flat_press', 'rest': 120},
            {'id': 2, 'name': 'Dumbbell Bench Press', 'muscle_group': 'chest', 'subcategory': 'mid_chest',
             'equipment': ['dumbbell', 'bench'], 'difficulty': 'beginner', 'type': 'compound',
             'category': 'flat_press', 'rest': 120},
            {'id': 3, 'name': 'Machine Chest Press', 'muscle_group': 'chest', 'subcategory': 'mid_chest',
             'equipment': ['machine'], 'difficulty': 'beginner', 'type': 'compound',
             'category': 'flat_press', 'rest': 90},
            {'id': 4, 'name': 'Incline Barbell Press', 'muscle_group': 'chest', 'subcategory': 'upper_chest',
             'equipment': ['barbell', 'bench', 'rack'], 'difficulty': 'intermediate', 'type': 'compound',
             'category': 'incline_press', 'rest': 120},
            {'id': 5, 'name': 'Incline Dumbbell Press', 'muscle_group': 'chest', 'subcategory': 'upper_chest',
             'equipment': ['dumbbell', 'bench'], 'difficulty': 'intermediate', 'type': 'compound',
             'category': 'incline_press', 'rest': 120},
            {'id': 6, 'name': 'Cable Flyes', 'muscle_group': 'chest', 'subcategory': 'mid_chest',
             'equipment': ['cable'], 'difficulty': 'intermediate', 'type': 'isolation',
             'category': 'chest_fly', 'rest': 60},
            {'id': 7, 'name': 'Pec Deck Flyes', 'muscle_group': 'chest', 'subcategory': 'mid_chest',
             'equipment': ['machine'], 'difficulty': 'beginner', 'type': 'isolation',
             'category': 'chest_fly', 'rest': 60},
            {'id': 8, 'name': 'Dips (Chest Focus)', 'muscle_group': 'chest', 'subcategory': 'lower_chest',
             'equipment': ['bodyweight'], 'difficulty': 'intermediate', 'type': 'compound',
             'category': 'dip', 'rest': 120},

            # BACK
            {'id': 9, 'name': 'Pull-Ups', 'muscle_group': 'back', 'equipment': ['pullup_bar'],
             'difficulty': 'intermediate', 'type': 'compound', 'category': 'vertical_pull', 'rest': 120},
            {'id': 10, 'name': 'Lat Pulldowns', 'muscle_group': 'back', 'equipment': ['cable', 'machine'],
             'difficulty': 'beginner', 'type': 'compound', 'category': 'vertical_pull', 'rest': 120},
            {'id': 11, 'name': 'Barbell Rows', 'muscle_group': 'back', 'equipment': ['barbell'],
             'difficulty': 'intermediate', 'type': 'compound', 'category': 'horizontal_pull', 'rest': 120},
            {'id': 12, 'name': 'Dumbbell Rows', 'muscle_group': 'back', 'equipment': ['dumbbell', 'bench'],
             'difficulty': 'beginner', 'type': 'compound', 'category': 'horizontal_pull', 'rest': 120},
            {'id': 13, 'name': 'Seated Cable Rows', 'muscle_group': 'back', 'equipment': ['cable'],
             'difficulty': 'beginner', 'type': 'compound', 'category': 'horizontal_pull', 'rest': 120},
            {'id': 14, 'name': 'Face Pulls', 'muscle_group': 'back', 'equipment': ['cable'],
             'difficulty': 'beginner', 'type': 'isolation', 'category': 'back_isolation', 'rest': 60},

            # LEGS
            {'id': 15, 'name': 'Barbell Back Squats', 'muscle_group': 'legs', 'subcategory': 'quads',
             'equipment': ['barbell', 'rack'], 'difficulty': 'intermediate', 'type': 'compound',
             'category': 'squat_pattern', 'rest': 180},
            {'id': 16, 'name': 'Leg Press', 'muscle_group': 'legs', 'equipment': ['machine'],
             'difficulty': 'beginner', 'type': 'compound', 'category': 'squat_pattern', 'rest': 120},
            {'id': 17, 'name': 'Hack Squats', 'muscle_group': 'legs', 'equipment': ['machine'],
             'difficulty': 'intermediate', 'type': 'compound', 'category': 'squat_pattern', 'rest': 120},
            {'id': 18, 'name': 'Goblet Squats', 'muscle_group': 'legs', 'equipment': ['dumbbell'],
             'difficulty': 'beginner', 'type': 'compound', 'category': 'squat_pattern', 'rest': 90},
            {'id': 19, 'name': 'Romanian Deadlifts', 'muscle_group': 'legs', 'equipment': ['barbell'],
             'difficulty': 'intermediate', 'type': 'compound', 'category': 'hip_hinge', 'rest': 120},
            {'id': 20, 'name': 'Dumbbell RDLs', 'muscle_group': 'legs', 'equipment': ['dumbbell'],
             'difficulty': 'beginner', 'type': 'compound', 'category': 'hip_hinge', 'rest': 120},
            {'id': 21, 'name': 'Leg Extensions', 'muscle_group': 'legs', 'equipment': ['machine'],
             'difficulty': 'beginner', 'type': 'isolation', 'category': 'quad_isolation', 'rest': 60},
            {'id': 22, 'name': 'Leg Curls', 'muscle_group': 'legs', 'equipment': ['machine'],
             'difficulty': 'beginner', 'type': 'isolation', 'category': 'hamstring_isolation', 'rest': 60},
            {'id': 23, 'name': 'Seated Leg Curls', 'muscle_group': 'legs', 'equipment': ['machine'],
             'difficulty': 'beginner', 'type': 'isolation', 'category': 'hamstring_isolation', 'rest': 60},
            {'id': 24, 'name': 'Bulgarian Split Squats', 'muscle_group': 'legs', 'equipment': ['dumbbell', 'bench'],
             'difficulty': 'intermediate', 'type': 'compound', 'category': 'unilateral_leg', 'rest': 90},
            {'id': 25, 'name': 'Walking Lunges', 'muscle_group': 'legs', 'equipment': ['dumbbell'],
             'difficulty': 'beginner', 'type': 'compound', 'category': 'unilateral_leg', 'rest': 90},

            # SHOULDERS
            {'id': 26, 'name': 'Overhead Press', 'muscle_group': 'shoulders', 'equipment': ['barbell', 'rack'],
             'difficulty': 'intermediate', 'type': 'compound', 'category': 'overhead_press', 'rest': 120},
            {'id': 27, 'name': 'Dumbbell Shoulder Press', 'muscle_group': 'shoulders', 'equipment': ['dumbbell'],
             'difficulty': 'beginner', 'type': 'compound', 'category': 'overhead_press', 'rest': 120},
            {'id': 28, 'name': 'Lateral Raises', 'muscle_group': 'shoulders', 'equipment': ['dumbbell'],
             'difficulty': 'beginner', 'type': 'isolation', 'category': 'lateral_delt', 'rest': 60},
            {'id': 29, 'name': 'Cable Lateral Raises', 'muscle_group': 'shoulders', 'equipment': ['cable'],
             'difficulty': 'beginner', 'type': 'isolation', 'category': 'lateral_delt', 'rest': 60},
            {'id': 30, 'name': 'Rear Delt Flyes', 'muscle_group': 'shoulders', 'equipment': ['dumbbell'],
             'difficulty': 'beginner', 'type': 'isolation', 'category': 'rear_delt', 'rest': 60},

            # ARMS
            {'id': 31, 'name': 'Barbell Curls', 'muscle_group': 'biceps', 'equipment': ['barbell'],
             'difficulty': 'beginner', 'type': 'isolation', 'category': 'bicep_curl', 'rest': 60},
            {'id': 32, 'name': 'Dumbbell Curls', 'muscle_group': 'biceps', 'equipment': ['dumbbell'],
             'difficulty': 'beginner', 'type': 'isolation', 'category': 'bicep_curl', 'rest': 60},
            {'id': 33, 'name': 'Hammer Curls', 'muscle_group': 'biceps', 'equipment': ['dumbbell'],
             'difficulty': 'beginner', 'type': 'isolation', 'category': 'bicep_curl', 'rest': 60},
            {'id': 34, 'name': 'Tricep Pushdowns', 'muscle_group': 'triceps', 'equipment': ['cable'],
             'difficulty': 'beginner', 'type': 'isolation', 'category': 'tricep_extension', 'rest': 60},
            {'id': 35, 'name': 'Overhead Tricep Extension', 'muscle_group': 'triceps', 'equipment': ['dumbbell'],
             'difficulty': 'beginner', 'type': 'isolation', 'category': 'tricep_extension', 'rest': 60},
            {'id': 36, 'name': 'Close-Grip Bench Press', 'muscle_group': 'triceps', 'equipment': ['barbell', 'bench'],
             'difficulty': 'intermediate', 'type': 'compound', 'category': 'tricep_press', 'rest': 90},

            # CORE
            {'id': 37, 'name': 'Planks', 'muscle_group': 'core', 'equipment': ['bodyweight'],
             'difficulty': 'beginner', 'type': 'isolation', 'category': 'core', 'rest': 60},
            {'id': 38, 'name': 'Cable Crunches', 'muscle_group': 'core', 'equipment': ['cable'],
             'difficulty': 'beginner', 'type': 'isolation', 'category': 'core', 'rest': 60}
        ]

    def generate_plan(self, goal, experience, equipment, days_per_week, session_duration=60, gender='male'):
        """Generate workout plan with gender-specific adjustments"""
        split = self._select_optimal_split(days_per_week, experience)
        available_exercises = self._filter_exercises(equipment, experience)
        params = self.goal_params[goal]
        volume_multiplier = self.experience_volume[experience]

        gender_focus = {
            'female': {'legs': 1.25, 'chest': 0.85, 'back': 0.95, 'shoulders': 0.90, 'biceps': 0.85, 'triceps': 0.85, 'core': 1.15},
            'male': {'legs': 1.0, 'chest': 1.0, 'back': 1.0, 'shoulders': 1.0, 'biceps': 1.0, 'triceps': 1.0, 'core': 1.0}
        }

        workouts = self._select_exercises_intelligently(split, available_exercises, params, volume_multiplier,
                                                       goal, gender_focus.get(gender, gender_focus['male']))
        progression = self._create_progression_plan(goal, experience)

        return {
            'split': split,
            'workouts': workouts,
            'progression': progression,
            'parameters': {'goal': goal, 'experience': experience, 'days_per_week': days_per_week,
                         'estimated_duration': session_duration, 'gender': gender}
        }

    def _select_optimal_split(self, days_per_week, experience):
        """Select training split based on frequency"""
        if days_per_week == 3:
            return {
                'name': 'Full Body 3x/week',
                'description': 'Full body training - optimal for beginners',
                'days': [
                    {'name': 'Full Body A', 'muscle_groups': ['chest', 'back', 'legs', 'shoulders', 'core']},
                    {'name': 'Full Body B', 'muscle_groups': ['legs', 'chest', 'back', 'biceps', 'triceps']},
                    {'name': 'Full Body C', 'muscle_groups': ['back', 'chest', 'legs', 'shoulders', 'core']}
                ]
            }
        elif days_per_week == 4:
            return {
                'name': 'Upper/Lower 4x/week',
                'description': 'Upper/Lower split',
                'days': [
                    {'name': 'Upper A', 'muscle_groups': ['chest', 'back', 'shoulders', 'biceps', 'triceps']},
                    {'name': 'Lower A', 'muscle_groups': ['legs', 'core']},
                    {'name': 'Upper B', 'muscle_groups': ['back', 'chest', 'shoulders', 'biceps', 'triceps']},
                    {'name': 'Lower B', 'muscle_groups': ['legs', 'core']}
                ]
            }
        elif days_per_week == 5:
            return {
                'name': 'Push/Pull/Legs 5x/week',
                'description': 'Push/Pull/Legs split',
                'days': [
                    {'name': 'Push A', 'muscle_groups': ['chest', 'shoulders', 'triceps']},
                    {'name': 'Pull A', 'muscle_groups': ['back', 'biceps']},
                    {'name': 'Legs A', 'muscle_groups': ['legs', 'core']},
                    {'name': 'Push B', 'muscle_groups': ['shoulders', 'chest', 'triceps']},
                    {'name': 'Pull B', 'muscle_groups': ['back', 'biceps', 'core']}
                ]
            }
        else:  # 6 days
            return {
                'name': 'Push/Pull/Legs 6x/week',
                'description': 'Push/Pull/Legs split - hitting each muscle 2x',
                'days': [
                    {'name': 'Push A', 'muscle_groups': ['chest', 'shoulders', 'triceps']},
                    {'name': 'Pull A', 'muscle_groups': ['back', 'biceps']},
                    {'name': 'Legs A', 'muscle_groups': ['legs', 'core']},
                    {'name': 'Push B', 'muscle_groups': ['chest', 'shoulders', 'triceps']},
                    {'name': 'Pull B', 'muscle_groups': ['back', 'biceps']},
                    {'name': 'Legs B', 'muscle_groups': ['legs', 'core']}
                ]
            }

    def _filter_exercises(self, equipment, experience):
        """Filter exercises by equipment and experience"""
        difficulty_levels = {
            'beginner': ['beginner'],
            'intermediate': ['beginner', 'intermediate'],
            'advanced': ['beginner', 'intermediate', 'advanced']
        }
        allowed_difficulties = difficulty_levels[experience]

        return [e for e in self.exercise_database
                if any(eq in equipment for eq in e['equipment']) and e['difficulty'] in allowed_difficulties]

    def _select_exercises_intelligently(self, split, available_exercises, params, volume_multiplier, goal, gender_focus):
        """Intelligent exercise selection with proper ordering"""
        workouts = []

        for day in split['days']:
            day_exercises = []
            for muscle_group in day['muscle_groups']:
                exercises_for_group = [e for e in available_exercises if e['muscle_group'] == muscle_group]
                if exercises_for_group:
                    gender_multiplier = gender_focus.get(muscle_group, 1.0)
                    selected = self._select_for_muscle_group(muscle_group, exercises_for_group, params,
                                                             volume_multiplier, gender_multiplier)
                    day_exercises.extend(selected)

            workouts.append({'day': day['name'], 'exercises': day_exercises})

        return workouts

    def _select_for_muscle_group(self, muscle_group, available_exercises, params, volume_multiplier, gender_multiplier=1.0):
        """Select exercises per muscle group with proper volume"""
        selected = []
        adjusted_volume = volume_multiplier * gender_multiplier

        categories = {
            'legs': ['hamstring_isolation', 'squat_pattern', 'hip_hinge', 'quad_isolation'],
            'chest': ['flat_press', 'incline_press', 'chest_fly'],
            'back': ['vertical_pull', 'horizontal_pull', 'back_isolation'],
            'shoulders': ['overhead_press', 'lateral_delt', 'rear_delt']
        }

        if muscle_group in categories:
            for idx, category in enumerate(categories[muscle_group]):
                matching = [e for e in available_exercises if e.get('category') == category]
                if matching:
                    exercise = matching[0]
                    sets = max(2, int(3 * adjusted_volume if idx < 2 else 2 * adjusted_volume))
                    selected.append({
                        'exercise': exercise,
                        'sets': sets,
                        'reps': f"{params['rep_range'][0]}-{params['rep_range'][1]}",
                        'rest_seconds': exercise['rest'],
                        'warmup_sets': '1-2 sets' if exercise['type'] == 'compound' else 'Optional',
                        'repsInReserve': params['rir']
                    })
        elif muscle_group in ['biceps', 'triceps', 'core']:
            for i, exercise in enumerate(available_exercises[:2 if muscle_group != 'core' else 1]):
                sets = max(2, int(3 * adjusted_volume if i == 0 else 2 * adjusted_volume))
                reps = '30-60s' if exercise['name'] == 'Planks' else f"{params['rep_range'][0]}-{params['rep_range'][1]}"
                selected.append({
                    'exercise': exercise,
                    'sets': sets,
                    'reps': reps,
                    'rest_seconds': exercise.get('rest', 60),
                    'warmup_sets': 'Not needed' if muscle_group == 'core' else 'Optional',
                    'repsInReserve': params['rir']
                })

        return selected

    def _create_progression_plan(self, goal, experience):
        """Create progression strategy"""
        plans = {
            'strength': {
                'method': 'Linear Progression',
                'increment': 'Increase weight by 2.5-5 lbs when you hit top of rep range',
                'deload': 'Deload 10% every 4 weeks',
                'tips': ['Focus on adding weight consistently', 'Rest 3-5 minutes between heavy sets', 'Maintain strict form']
            },
            'hypertrophy': {
                'method': 'Double Progression',
                'increment': 'Increase reps until you hit 12, then add weight and drop to 8 reps',
                'deload': 'Deload 20% every 5-6 weeks',
                'tips': ['Train 1-2 reps from failure', 'Focus on mind-muscle connection', 'Track workouts for progressive overload']
            },
            'endurance': {
                'method': 'Rep Progression',
                'increment': 'Add 1-2 reps per week',
                'deload': 'Deload every 6 weeks',
                'tips': ['Keep rest periods short', 'Focus on time under tension']
            },
            'weight_loss': {
                'method': 'Maintenance + Metabolic',
                'increment': 'Maintain strength in deficit',
                'deload': 'Deload as needed',
                'tips': ['Prioritize maintaining strength', 'Keep protein high', 'Shorter rest periods for calorie burn']
            }
        }

        progression = plans[goal].copy()
        if experience == 'beginner':
            progression['tips'].insert(0, 'Focus on learning proper form')
            progression['tips'].insert(1, 'Expect rapid progress in first 3-6 months')
        elif experience == 'advanced':
            progression['tips'].append('Consider periodization')

        return progression

    def get_exercise_database(self):
        """Return exercise database"""
        return self.exercise_database
