import numpy as np
import os

# Force TensorFlow to use CPU (avoids GPU/CUDA issues)
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

import tensorflow as tf
from tensorflow import keras

class CalorieCalculator:
    """
    AI-powered calorie calculator using TensorFlow neural network
    Calculates maintenance calories and macronutrient breakdown
    """

    def __init__(self):
        self.model = self._build_model()
        self.activity_multipliers = {
            'sedentary': 1.2,
            'light': 1.375,
            'moderate': 1.55,
            'active': 1.725,
            'very_active': 1.9
        }

        self.goal_adjustments = {
            'lose': -500,  # 500 calorie deficit
            'maintain': 0,
            'gain': 300    # 300 calorie surplus
        }

    def _build_model(self):
        """
        Build TensorFlow neural network for calorie prediction
        Input features: age, height, weight, gender_encoded, activity_level_encoded
        Output: BMR (Basal Metabolic Rate)
        """
        model = keras.Sequential([
            keras.layers.Dense(64, activation='relu', input_shape=(5,)),
            keras.layers.Dropout(0.2),
            keras.layers.Dense(32, activation='relu'),
            keras.layers.Dropout(0.1),
            keras.layers.Dense(16, activation='relu'),
            keras.layers.Dense(1, activation='linear')  # BMR output
        ])

        model.compile(
            optimizer='adam',
            loss='mse',
            metrics=['mae']
        )

        # Initialize with pre-trained weights if available
        model_path = os.path.join(os.path.dirname(__file__), 'calorie_model.h5')
        if os.path.exists(model_path):
            model.load_weights(model_path)
        else:
            # Train on synthetic data for initial deployment
            self._train_initial_model(model)

        return model

    def _train_initial_model(self, model):
        """
        Train model on synthetic data based on established BMR formulas
        Uses Mifflin-St Jeor equation as ground truth
        """
        # Generate synthetic training data
        np.random.seed(42)
        n_samples = 10000

        # Generate realistic ranges
        ages = np.random.randint(18, 70, n_samples)
        heights = np.random.uniform(150, 200, n_samples)  # cm
        weights = np.random.uniform(50, 120, n_samples)   # kg
        genders = np.random.randint(0, 2, n_samples)      # 0=female, 1=male
        activity_levels = np.random.uniform(0, 1, n_samples)

        # Calculate BMR using Mifflin-St Jeor equation
        bmr = np.zeros(n_samples)
        for i in range(n_samples):
            if genders[i] == 1:  # male
                bmr[i] = 10 * weights[i] + 6.25 * heights[i] - 5 * ages[i] + 5
            else:  # female
                bmr[i] = 10 * weights[i] + 6.25 * heights[i] - 5 * ages[i] - 161

        # Prepare training data
        X = np.column_stack([ages, heights, weights, genders, activity_levels])
        y = bmr

        # Train model
        model.fit(X, y, epochs=50, batch_size=32, verbose=0, validation_split=0.2)

        # Save trained model
        model_path = os.path.join(os.path.dirname(__file__), 'calorie_model.h5')
        model.save_weights(model_path)

    def calculate(self, age, height, weight, gender, activity_level, goal):
        """
        Calculate maintenance calories and macronutrient breakdown

        Args:
            age: int, years
            height: float, cm
            weight: float, kg
            gender: str, 'male' or 'female'
            activity_level: str, activity level key
            goal: str, 'lose', 'maintain', or 'gain'

        Returns:
            dict with calorie and macro information
        """
        # Encode inputs
        gender_encoded = 1 if gender.lower() == 'male' else 0
        activity_encoded = list(self.activity_multipliers.keys()).index(activity_level) / 4.0

        # Prepare input for model
        input_data = np.array([[age, height, weight, gender_encoded, activity_encoded]])

        # Predict BMR using neural network
        bmr_predicted = self.model.predict(input_data, verbose=0)[0][0]

        # Also calculate using Mifflin-St Jeor for validation
        if gender.lower() == 'male':
            bmr_formula = 10 * weight + 6.25 * height - 5 * age + 5
        else:
            bmr_formula = 10 * weight + 6.25 * height - 5 * age - 161

        # Use weighted average of ML prediction and formula
        bmr = 0.7 * bmr_predicted + 0.3 * bmr_formula

        # Calculate TDEE (Total Daily Energy Expenditure)
        activity_multiplier = self.activity_multipliers[activity_level]
        tdee = bmr * activity_multiplier

        # Adjust for goal
        goal_adjustment = self.goal_adjustments[goal]
        target_calories = tdee + goal_adjustment

        # Calculate macronutrient breakdown
        macros = self._calculate_macros(target_calories, weight, goal)

        return {
            'bmr': round(bmr, 1),
            'tdee': round(tdee, 1),
            'target_calories': round(target_calories, 1),
            'goal': goal,
            'macros': macros,
            'recommendations': self._get_recommendations(goal, target_calories)
        }

    def _calculate_macros(self, calories, weight, goal):
        """
        Calculate optimal macronutrient breakdown

        Protein: 1.8-2.2g per kg bodyweight (higher for cutting)
        Fats: 25-30% of total calories
        Carbs: Remaining calories
        """
        # Protein calculation
        if goal == 'lose':
            protein_per_kg = 2.2  # Higher protein for muscle preservation
        elif goal == 'gain':
            protein_per_kg = 2.0
        else:
            protein_per_kg = 1.8

        protein_grams = weight * protein_per_kg
        protein_calories = protein_grams * 4

        # Fat calculation (25-30% of calories)
        fat_percentage = 0.28
        fat_calories = calories * fat_percentage
        fat_grams = fat_calories / 9

        # Carbs get remaining calories
        carb_calories = calories - protein_calories - fat_calories
        carb_grams = carb_calories / 4

        return {
            'protein': {
                'grams': round(protein_grams, 1),
                'calories': round(protein_calories, 1),
                'percentage': round((protein_calories / calories) * 100, 1)
            },
            'carbs': {
                'grams': round(carb_grams, 1),
                'calories': round(carb_calories, 1),
                'percentage': round((carb_calories / calories) * 100, 1)
            },
            'fats': {
                'grams': round(fat_grams, 1),
                'calories': round(fat_calories, 1),
                'percentage': round((fat_calories / calories) * 100, 1)
            }
        }

    def _get_recommendations(self, goal, calories):
        """Generate personalized recommendations based on goal"""
        recommendations = []

        if goal == 'lose':
            recommendations.append("Aim for 0.5-1kg weight loss per week for sustainable results")
            recommendations.append("Prioritize protein to preserve muscle mass during deficit")
            recommendations.append("Include resistance training 3-4x per week")
        elif goal == 'gain':
            recommendations.append("Aim for 0.25-0.5kg weight gain per week to minimize fat gain")
            recommendations.append("Progressive overload in training is essential")
            recommendations.append("Spread protein intake across 4-5 meals daily")
        else:
            recommendations.append("Monitor weight weekly and adjust calories if needed")
            recommendations.append("Focus on body composition over scale weight")

        recommendations.append(f"Drink at least 3L of water daily")
        recommendations.append("Track your intake for at least 2 weeks to establish patterns")

        return recommendations
