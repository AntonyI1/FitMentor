# Machine Learning Improvement Guide

This document explains how FitMentor's ML models continuously improve over time.

## How It Works

### 1. Data Collection
Every time a user:
- Calculates their calories
- Generates a workout plan

The input and output data is automatically saved to:
- `backend/data/calorie_calculations.jsonl`
- `backend/data/workout_plans.jsonl`

This data is used to retrain and improve the ML models.

### 2. Model Architecture

**Calorie Calculator (TensorFlow)**
- Input: age, height, weight, gender, activity level
- Architecture: 64→32→16→1 neurons
- Output: BMR prediction
- Current training: 10,000 synthetic samples (Mifflin-St Jeor formula)
- Future: Will be retrained on real user data

**Workout Suggester (PyTorch)**
- Input: goal, experience, equipment, frequency
- Architecture: 128→64 neurons with dropout
- Output: Exercise selection scores
- Continuously learns from user preferences

### 3. Retraining Process

When you have enough collected data, retrain the models:

```bash
cd backend
python retrain_models.py
```

**Minimum data requirements:**
- Calorie model: 100+ samples
- Workout model: 50+ samples

**What happens during retraining:**
1. Loads all collected user data
2. Prepares training/validation sets
3. Retrains neural networks
4. Saves improved model weights
5. Shows training metrics

### 4. Checking Progress

View how much data has been collected:

**Via API:**
```bash
curl http://localhost:5000/api/stats
```

**Via Python:**
```python
from models.data_collector import DataCollector

collector = DataCollector()
print(f"Calorie data: {collector.get_calorie_data_count()}")
print(f"Workout data: {collector.get_workout_data_count()}")
```

### 5. Model Improvement Cycle

```
User Input → ML Prediction → Save Data → Accumulate Samples → Retrain → Better Predictions
     ↑                                                                          |
     └──────────────────────────────────────────────────────────────────────────┘
```

## Why This Approach?

### Advantages over Simple Formulas

1. **Personalization**: Learns patterns specific to your user base
2. **Continuous Improvement**: Gets better over time
3. **Adaptation**: Can adapt to new trends and data
4. **Portfolio Value**: Demonstrates real ML skills
5. **Scalability**: Ready for production deployment

### Initial Training vs Future Training

**Initial (Synthetic Data)**
- Based on proven formulas
- 10,000 samples
- Good baseline accuracy

**Future (Real Data)**
- Based on actual users
- Learns real-world patterns
- Can discover insights formulas miss
- Personalized to your audience

## Advanced: Custom Training

You can also train on external datasets:

```python
from models.calorie_calculator import CalorieCalculator
import numpy as np

# Your custom training data
X_train = np.array([[25, 175, 75, 1, 0.5], ...])  # age, height, weight, gender, activity
y_train = np.array([1750, ...])  # actual BMR values

# Train model
calc = CalorieCalculator()
calc.model.fit(X_train, y_train, epochs=100, batch_size=32)

# Save
calc.model.save_weights('backend/models/calorie_model.h5')
```

## Monitoring Model Performance

After retraining, compare metrics:

1. **Training Loss**: Should decrease
2. **Validation Loss**: Should decrease (watch for overfitting)
3. **MAE (Mean Absolute Error)**: Lower is better
4. **Real-world Testing**: Test with known cases

## Best Practices

1. **Collect diverse data**: Different ages, weights, goals
2. **Retrain regularly**: Every 100-500 new samples
3. **Validate results**: Spot-check predictions after retraining
4. **Backup models**: Save old weights before retraining
5. **Monitor performance**: Track prediction accuracy over time

## Data Privacy

- All data is stored locally
- No personal identifiers saved
- Only training inputs/outputs collected
- Users anonymous by default

## Future Enhancements

Potential improvements:
- Add user feedback loop (was prediction accurate?)
- Implement A/B testing of model versions
- Add model versioning and rollback
- Create automated retraining pipeline
- Deploy models to cloud for scaling

---

**The ML approach makes FitMentor a living system that improves with every user interaction.**
