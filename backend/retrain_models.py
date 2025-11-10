"""
Script to retrain ML models with collected user data
Run this periodically to improve model accuracy
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.data_collector import DataCollector
from models.calorie_calculator import CalorieCalculator
import numpy as np

def retrain_calorie_model():
    """Retrain calorie calculator with collected data"""
    print("\n" + "="*50)
    print("Retraining Calorie Calculator Model")
    print("="*50)

    collector = DataCollector()
    data = collector.load_calorie_data()

    if len(data) < 100:
        print(f"\n⚠ Only {len(data)} samples collected.")
        print("Need at least 100 samples for retraining.")
        print("Continue using current model.")
        return False

    print(f"\n✓ Found {len(data)} samples for training")

    # Prepare training data
    X = []
    y = []

    for record in data:
        inp = record['input']
        out = record['output']

        # Encode features
        gender_encoded = 1 if inp['gender'].lower() == 'male' else 0
        activity_levels = ['sedentary', 'light', 'moderate', 'active', 'very_active']
        activity_encoded = activity_levels.index(inp['activity_level']) / 4.0

        features = [
            inp['age'],
            inp['height'],
            inp['weight'],
            gender_encoded,
            activity_encoded
        ]

        X.append(features)
        y.append(out['bmr'])

    X = np.array(X)
    y = np.array(y)

    print(f"\nTraining data shape: {X.shape}")

    # Retrain model
    calc = CalorieCalculator()
    model = calc.model

    print("\nTraining model...")
    history = model.fit(X, y, epochs=100, batch_size=32, verbose=1, validation_split=0.2)

    # Save retrained model
    model_path = os.path.join(os.path.dirname(__file__), 'models/calorie_model.weights.h5')
    model.save_weights(model_path)

    print(f"\n✓ Model retrained and saved to {model_path}")
    print(f"Final loss: {history.history['loss'][-1]:.2f}")
    print(f"Final validation loss: {history.history['val_loss'][-1]:.2f}")

    return True


def retrain_workout_model():
    """Retrain workout suggester with collected data"""
    print("\n" + "="*50)
    print("Retraining Workout Suggester Model")
    print("="*50)

    collector = DataCollector()
    data = collector.load_workout_data()

    if len(data) < 50:
        print(f"\n⚠ Only {len(data)} samples collected.")
        print("Need at least 50 samples for retraining.")
        print("Continue using current model.")
        return False

    print(f"\n✓ Found {len(data)} samples")
    print("Workout model retraining requires more complex logic.")
    print("For now, data is being collected for future improvement.")

    return True


def main():
    print("\n" + "="*50)
    print("FitMentor Model Retraining")
    print("="*50)

    collector = DataCollector()
    calorie_count = collector.get_calorie_data_count()
    workout_count = collector.get_workout_data_count()

    print(f"\nCollected data:")
    print(f"  Calorie calculations: {calorie_count}")
    print(f"  Workout plans: {workout_count}")

    if calorie_count == 0 and workout_count == 0:
        print("\n⚠ No data collected yet.")
        print("Use the application to generate training data first.")
        return

    # Retrain models
    calorie_retrained = retrain_calorie_model()
    workout_retrained = retrain_workout_model()

    print("\n" + "="*50)
    print("Retraining Summary")
    print("="*50)
    print(f"Calorie model: {'✓ Retrained' if calorie_retrained else '- Not enough data'}")
    print(f"Workout model: {'✓ Retrained' if workout_retrained else '- Not enough data'}")

    if calorie_retrained or workout_retrained:
        print("\n✓ Restart the server to use updated models")


if __name__ == "__main__":
    main()
