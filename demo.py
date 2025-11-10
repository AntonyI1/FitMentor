#!/usr/bin/env python3
"""
FitMentor Demo - Shows what the app does without requiring Flask/TensorFlow
Run this to see the functionality before installing dependencies
"""

def calculate_calories_demo():
    """Demo of calorie calculator"""
    print("\n" + "="*60)
    print("CALORIE CALCULATOR DEMO")
    print("="*60)

    # Sample user input
    age = 25
    height = 175  # cm
    weight = 75   # kg
    gender = 'male'
    activity_level = 'moderate'
    goal = 'maintain'

    print(f"\nInput:")
    print(f"  Age: {age} years")
    print(f"  Height: {height} cm")
    print(f"  Weight: {weight} kg")
    print(f"  Gender: {gender}")
    print(f"  Activity: {activity_level}")
    print(f"  Goal: {goal}")

    # Calculate BMR (Mifflin-St Jeor formula)
    if gender == 'male':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    # Activity multipliers
    activity_multipliers = {
        'sedentary': 1.2,
        'light': 1.375,
        'moderate': 1.55,
        'active': 1.725,
        'very_active': 1.9
    }

    tdee = bmr * activity_multipliers[activity_level]

    # Goal adjustments
    goal_adjustments = {
        'lose': -500,
        'maintain': 0,
        'gain': 300
    }

    target_calories = tdee + goal_adjustments[goal]

    # Calculate macros
    protein_per_kg = 1.8
    protein_grams = weight * protein_per_kg
    protein_calories = protein_grams * 4

    fat_calories = target_calories * 0.28
    fat_grams = fat_calories / 9

    carb_calories = target_calories - protein_calories - fat_calories
    carb_grams = carb_calories / 4

    print(f"\n✓ Results:")
    print(f"  BMR: {bmr:.1f} kcal")
    print(f"  TDEE: {tdee:.1f} kcal")
    print(f"  Target Calories: {target_calories:.1f} kcal")

    print(f"\n  Macros:")
    print(f"    Protein: {protein_grams:.1f}g ({protein_calories:.0f} kcal)")
    print(f"    Carbs: {carb_grams:.1f}g ({carb_calories:.0f} kcal)")
    print(f"    Fats: {fat_grams:.1f}g ({fat_calories:.0f} kcal)")

    print(f"\n  Recommendations:")
    print(f"    - Monitor weight weekly")
    print(f"    - Drink at least 3L water daily")
    print(f"    - Track intake for 2 weeks")


def workout_suggester_demo():
    """Demo of workout suggester"""
    print("\n" + "="*60)
    print("WORKOUT SUGGESTER DEMO")
    print("="*60)

    # Sample input
    goal = 'hypertrophy'
    experience = 'intermediate'
    equipment = ['barbell', 'dumbbell', 'bench']
    days_per_week = 4

    print(f"\nInput:")
    print(f"  Goal: {goal}")
    print(f"  Experience: {experience}")
    print(f"  Equipment: {', '.join(equipment)}")
    print(f"  Days per week: {days_per_week}")

    print(f"\n✓ Generated Plan:")
    print(f"  Split: Upper/Lower (4 days)")

    print(f"\n  Day 1 - Upper A:")
    print(f"    1. Barbell Bench Press: 4 × 8-12 (90s rest)")
    print(f"    2. Barbell Rows: 4 × 8-12 (90s rest)")
    print(f"    3. Dumbbell Shoulder Press: 3 × 10-12 (90s rest)")
    print(f"    4. Dumbbell Curl: 3 × 10-12 (60s rest)")

    print(f"\n  Day 2 - Lower A:")
    print(f"    1. Barbell Squat: 4 × 8-12 (90s rest)")
    print(f"    2. Romanian Deadlift: 3 × 10-12 (90s rest)")
    print(f"    3. Lunges: 3 × 12-15 (60s rest)")

    print(f"\n  Day 3 - Upper B:")
    print(f"    1. Incline Dumbbell Press: 4 × 8-12 (90s rest)")
    print(f"    2. Pull-ups: 3 × 8-12 (90s rest)")
    print(f"    3. Lateral Raises: 3 × 12-15 (60s rest)")

    print(f"\n  Day 4 - Lower B:")
    print(f"    1. Leg Press: 4 × 10-12 (90s rest)")
    print(f"    2. Leg Curl: 3 × 10-12 (60s rest)")
    print(f"    3. Calf Raises: 3 × 15-20 (45s rest)")

    print(f"\n  Progression:")
    print(f"    - Method: Progressive overload with volume")
    print(f"    - Increase reps or weight each week")
    print(f"    - Deload every 6-8 weeks")


def main():
    print("\n" + "="*60)
    print("        FitMentor - AI Fitness Coach Demo")
    print("="*60)
    print("\nThis demo shows what the app does WITHOUT requiring")
    print("Flask, TensorFlow, or PyTorch installation.")
    print("\nThe actual app uses:")
    print("  • TensorFlow neural networks for calorie prediction")
    print("  • PyTorch models for workout exercise selection")
    print("  • Flask REST API for backend")
    print("  • Modern web UI for frontend")
    print("  • Data collection for continuous ML improvement")

    calculate_calories_demo()
    workout_suggester_demo()

    print("\n" + "="*60)
    print("To run the ACTUAL app:")
    print("="*60)
    print("\n1. Install dependencies:")
    print("   ./setup.sh")
    print("\n2. Start backend:")
    print("   ./run.sh")
    print("\n3. Open frontend:")
    print("   http://localhost:8000")
    print("\n" + "="*60)


if __name__ == "__main__":
    main()
