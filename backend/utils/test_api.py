"""
Test script for FitMentor API endpoints
Run this to verify the API is working correctly
"""

import requests
import json

API_BASE_URL = "http://localhost:5000/api"

def test_calorie_calculator():
    """Test calorie calculator endpoint"""
    print("\n" + "="*50)
    print("Testing Calorie Calculator")
    print("="*50)

    test_data = {
        "age": 25,
        "height": 175,
        "weight": 75,
        "gender": "male",
        "activity_level": "moderate",
        "goal": "gain"
    }

    try:
        response = requests.post(
            f"{API_BASE_URL}/calculate-calories",
            json=test_data
        )
        response.raise_for_status()

        result = response.json()

        print("\nInput Data:")
        for key, value in test_data.items():
            print(f"  {key}: {value}")

        print("\nResults:")
        print(f"  BMR: {result['bmr']} kcal")
        print(f"  TDEE: {result['tdee']} kcal")
        print(f"  Target Calories: {result['target_calories']} kcal")

        print("\nMacronutrients:")
        macros = result['macros']
        print(f"  Protein: {macros['protein']['grams']}g ({macros['protein']['percentage']}%)")
        print(f"  Carbs: {macros['carbs']['grams']}g ({macros['carbs']['percentage']}%)")
        print(f"  Fats: {macros['fats']['grams']}g ({macros['fats']['percentage']}%)")

        print("\nRecommendations:")
        for rec in result['recommendations']:
            print(f"  - {rec}")

        print("\n✓ Calorie Calculator Test PASSED")
        return True

    except requests.exceptions.ConnectionError:
        print("\n✗ Error: Cannot connect to API. Is the server running?")
        return False
    except Exception as e:
        print(f"\n✗ Calorie Calculator Test FAILED: {str(e)}")
        return False


def test_workout_suggester():
    """Test workout suggester endpoint"""
    print("\n" + "="*50)
    print("Testing Workout Suggester")
    print("="*50)

    test_data = {
        "goal": "hypertrophy",
        "experience": "intermediate",
        "equipment": ["barbell", "dumbbell", "bench", "cable"],
        "days_per_week": 4,
        "session_duration": 60
    }

    try:
        response = requests.post(
            f"{API_BASE_URL}/suggest-workout",
            json=test_data
        )
        response.raise_for_status()

        result = response.json()

        print("\nInput Data:")
        for key, value in test_data.items():
            print(f"  {key}: {value}")

        print(f"\nGenerated Plan:")
        print(f"  Split: {result['split']['name']}")
        print(f"  Goal: {result['parameters']['goal']}")
        print(f"  Days per week: {result['parameters']['days_per_week']}")

        print(f"\nWorkout Days: {len(result['workouts'])}")
        for workout in result['workouts']:
            print(f"\n  {workout['day']}:")
            print(f"    Exercises: {len(workout['exercises'])}")
            for ex in workout['exercises'][:3]:  # Show first 3 exercises
                print(f"      - {ex['exercise']['name']}: {ex['sets']} × {ex['reps']}")

        print(f"\nProgression Strategy:")
        prog = result['progression']
        print(f"  Method: {prog['method']}")
        print(f"  Increment: {prog['increment']}")

        print("\n✓ Workout Suggester Test PASSED")
        return True

    except requests.exceptions.ConnectionError:
        print("\n✗ Error: Cannot connect to API. Is the server running?")
        return False
    except Exception as e:
        print(f"\n✗ Workout Suggester Test FAILED: {str(e)}")
        return False


def test_exercise_database():
    """Test exercise database endpoint"""
    print("\n" + "="*50)
    print("Testing Exercise Database")
    print("="*50)

    try:
        response = requests.get(f"{API_BASE_URL}/exercises")
        response.raise_for_status()

        result = response.json()

        print(f"\nTotal Exercises: {result['total_exercises']}")
        print(f"Muscle Groups: {', '.join(result['muscle_groups'])}")
        print(f"Equipment Types: {', '.join(result['equipment_types'])}")

        print("\nSample Exercises:")
        for ex in result['exercises'][:5]:
            print(f"  - {ex['name']} ({ex['muscle_group']})")

        print("\n✓ Exercise Database Test PASSED")
        return True

    except requests.exceptions.ConnectionError:
        print("\n✗ Error: Cannot connect to API. Is the server running?")
        return False
    except Exception as e:
        print(f"\n✗ Exercise Database Test FAILED: {str(e)}")
        return False


def main():
    print("\n" + "="*50)
    print("FitMentor API Test Suite")
    print("="*50)
    print("Ensure the backend server is running on http://localhost:5000")

    results = {
        'Calorie Calculator': test_calorie_calculator(),
        'Workout Suggester': test_workout_suggester(),
        'Exercise Database': test_exercise_database()
    }

    print("\n" + "="*50)
    print("Test Summary")
    print("="*50)
    for test_name, passed in results.items():
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{test_name}: {status}")

    all_passed = all(results.values())
    if all_passed:
        print("\n✓ All tests passed successfully!")
    else:
        print("\n✗ Some tests failed. Please check the output above.")

    return all_passed


if __name__ == "__main__":
    main()
