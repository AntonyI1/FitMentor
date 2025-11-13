"""
Evidence-Based Calorie Calculator
Uses Mifflin-St Jeor equation (gold standard for BMR calculation)
Protein based on bodyweight: 1.0g per lb (research-backed target)

TODO: Train ML model on real user data for personalization
"""

import numpy as np
import os

os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

import tensorflow as tf
from tensorflow import keras


class CalorieCalculator:
    def __init__(self):
        self.activity_multipliers = {
            'sedentary': 1.2,
            'light': 1.375,
            'moderate': 1.55,
            'active': 1.725,
            'very_active': 1.9
        }

        self.goal_adjustments = {
            'lose': -500,    # 500 kcal deficit = ~1 lb/week loss
            'maintain': 0,
            'gain': 300      # 300 kcal surplus = lean muscle gain
        }

        self.protein_targets = {
            'lose': 1.0,     # 1.0g/lb - preserves muscle in deficit
            'maintain': 1.0,
            'gain': 1.0
        }

        self.fat_minimum_ratio = 0.25  # At least 25% of calories from fat

        # TODO: Lazy-load ML model when trained weights available
        self.model = None

    def _build_model(self):
        """Build TensorFlow neural network for future personalized calorie prediction"""
        model = keras.Sequential([
            keras.layers.Dense(64, activation='relu', input_shape=(5,)),
            keras.layers.Dropout(0.2),
            keras.layers.Dense(32, activation='relu'),
            keras.layers.Dropout(0.1),
            keras.layers.Dense(16, activation='relu'),
            keras.layers.Dense(1, activation='linear')
        ])

        model.compile(optimizer='adam', loss='mse', metrics=['mae'])

        # TODO: Load trained weights
        # model_path = os.path.join(os.path.dirname(__file__), 'calorie_model.weights.h5')
        # if os.path.exists(model_path):
        #     model.load_weights(model_path)

        return model

    def calculate(self, age, height, weight, gender, activity_level, goal):
        """Calculate personalized calorie and macro targets using Mifflin-St Jeor equation"""
        bmr = self._calculate_bmr(age, height, weight, gender)

        # TODO: Apply ML model adjustment when available
        # if self.model is not None:
        #     features = self._encode_features(age, height, weight, gender, activity_level)
        #     adjustment_factor = self.model.predict(features, verbose=0)[0][0]
        #     bmr *= adjustment_factor

        activity_multiplier = self.activity_multipliers.get(activity_level, 1.2)
        tdee = int(bmr * activity_multiplier)

        goal_adjustment = self.goal_adjustments.get(goal, 0)
        target_calories = tdee + goal_adjustment

        weight_lbs = weight * 2.20462
        macros = self._calculate_macros(target_calories, goal, weight_lbs)
        recommendations = self._generate_recommendations(goal, activity_level, target_calories)

        return {
            'bmr': int(bmr),
            'tdee': tdee,
            'target_calories': target_calories,
            'macros': macros,
            'recommendations': recommendations
        }

    def _calculate_bmr(self, age, height, weight, gender):
        """Calculate BMR using Mifflin-St Jeor equation"""
        if gender == 'male':
            return 10 * weight + 6.25 * height - 5 * age + 5
        else:
            return 10 * weight + 6.25 * height - 5 * age - 161

    def _calculate_macros(self, target_calories, goal, weight_lbs):
        """Calculate macronutrient breakdown based on bodyweight and goal"""
        # Protein: 1.0g per lb bodyweight
        protein_per_lb = self.protein_targets[goal]
        protein_grams = int(weight_lbs * protein_per_lb)
        protein_calories = protein_grams * 4

        # Fat: minimum 25% of calories for hormonal health
        fat_calories = int(target_calories * self.fat_minimum_ratio)
        fat_grams = int(fat_calories / 9)

        # Carbs: remaining calories
        carbs_calories = target_calories - protein_calories - fat_calories
        carbs_grams = int(carbs_calories / 4)

        protein_percentage = int((protein_calories / target_calories) * 100)
        carbs_percentage = int((carbs_calories / target_calories) * 100)
        fats_percentage = int((fat_calories / target_calories) * 100)

        return {
            'protein': {'grams': protein_grams, 'calories': protein_calories, 'percentage': protein_percentage},
            'carbs': {'grams': carbs_grams, 'calories': carbs_calories, 'percentage': carbs_percentage},
            'fats': {'grams': fat_grams, 'calories': fat_calories, 'percentage': fats_percentage}
        }

    def _generate_recommendations(self, goal, activity_level, target_calories):
        """Generate personalized nutrition recommendations"""
        recommendations = []

        if goal == 'lose':
            recommendations.extend([
                f"Aim for {target_calories} calories per day for sustainable 1 lb/week weight loss",
                "Protein at 1.0g per lb bodyweight to preserve muscle",
                "Track weight weekly and adjust calories if progress stalls for 2+ weeks",
                "Include 2-3 strength training sessions per week"
            ])
        elif goal == 'gain':
            recommendations.extend([
                f"Aim for {target_calories} calories per day for lean muscle gain",
                "Protein at 1.0g per lb bodyweight to support muscle growth",
                "Time carbs around workouts for optimal performance",
                "Gain 0.5-1 lb per week; adjust if gaining faster"
            ])
        else:  # maintain
            recommendations.extend([
                f"Maintain {target_calories} calories per day",
                "Protein at 1.0g per lb bodyweight for muscle maintenance",
                "Continue strength training to maintain or build muscle",
                "Monitor weight weekly and adjust if trending"
            ])

        if activity_level in ['active', 'very_active']:
            recommendations.extend([
                "Ensure adequate carbs for recovery and performance",
                "Post-workout meal with protein and carbs within 2 hours"
            ])

        recommendations.extend([
            "Spread protein across 3-4 meals for optimal synthesis",
            "Stay hydrated: 0.5-1 oz water per lb bodyweight daily",
            "Prioritize whole foods: vegetables, fruits, lean proteins, whole grains, healthy fats"
        ])

        return recommendations

    def _encode_features(self, age, height, weight, gender, activity_level):
        """Encode features for ML model input (when ML model is used)"""
        gender_encoded = 1 if gender == 'male' else 0
        activity_encoded = {
            'sedentary': 0.0,
            'light': 0.25,
            'moderate': 0.5,
            'active': 0.75,
            'very_active': 1.0
        }.get(activity_level, 0.5)

        return np.array([[age, height, weight, gender_encoded, activity_encoded]])
