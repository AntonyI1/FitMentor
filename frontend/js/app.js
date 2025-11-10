// API Configuration
const API_BASE_URL = 'http://localhost:5000/api';

// DOM Elements - Calorie Calculator
const calorieForm = document.getElementById('calorieForm');
const calorieResults = document.getElementById('calorieResults');
const loadingOverlay = document.getElementById('loading');

// DOM Elements - Workout Suggester
const workoutForm = document.getElementById('workoutForm');
const workoutResults = document.getElementById('workoutResults');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    smoothScroll();
});

function setupEventListeners() {
    // Calorie Calculator Form
    calorieForm.addEventListener('submit', handleCalorieSubmit);

    // Workout Form
    workoutForm.addEventListener('submit', handleWorkoutSubmit);
}

// Smooth scroll for navigation
function smoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Calorie Calculator Functions
async function handleCalorieSubmit(e) {
    e.preventDefault();

    const formData = {
        age: parseInt(document.getElementById('age').value),
        height: parseFloat(document.getElementById('height').value),
        weight: parseFloat(document.getElementById('weight').value),
        gender: document.getElementById('gender').value,
        activity_level: document.getElementById('activity').value,
        goal: document.getElementById('goal').value
    };

    showLoading(true);

    try {
        const response = await fetch(`${API_BASE_URL}/calculate-calories`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        if (!response.ok) {
            throw new Error('Failed to calculate calories');
        }

        const data = await response.json();
        displayCalorieResults(data);

    } catch (error) {
        console.error('Error:', error);
        alert('Error calculating calories. Please make sure the backend server is running.');
    } finally {
        showLoading(false);
    }
}

function displayCalorieResults(data) {
    // Show results card
    calorieResults.classList.remove('hidden');

    // Update main values
    document.getElementById('bmr').textContent = `${data.bmr} kcal`;
    document.getElementById('tdee').textContent = `${data.tdee} kcal`;
    document.getElementById('targetCalories').textContent = `${data.target_calories} kcal`;

    // Update macros
    const macros = data.macros;

    // Protein
    document.getElementById('proteinValue').textContent =
        `${macros.protein.grams}g (${macros.protein.percentage}%)`;
    document.getElementById('proteinBar').style.width = `${macros.protein.percentage}%`;

    // Carbs
    document.getElementById('carbsValue').textContent =
        `${macros.carbs.grams}g (${macros.carbs.percentage}%)`;
    document.getElementById('carbsBar').style.width = `${macros.carbs.percentage}%`;

    // Fats
    document.getElementById('fatsValue').textContent =
        `${macros.fats.grams}g (${macros.fats.percentage}%)`;
    document.getElementById('fatsBar').style.width = `${macros.fats.percentage}%`;

    // Update recommendations
    const recommendationsList = document.getElementById('recommendationsList');
    recommendationsList.innerHTML = '';
    data.recommendations.forEach(rec => {
        const li = document.createElement('li');
        li.textContent = rec;
        recommendationsList.appendChild(li);
    });

    // Scroll to results
    calorieResults.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Workout Suggester Functions
async function handleWorkoutSubmit(e) {
    e.preventDefault();

    // Get selected equipment
    const equipmentCheckboxes = document.querySelectorAll('input[name="equipment"]:checked');
    const equipment = Array.from(equipmentCheckboxes).map(cb => cb.value);

    if (equipment.length === 0) {
        alert('Please select at least one equipment option');
        return;
    }

    const formData = {
        goal: document.getElementById('workoutGoal').value,
        experience: document.getElementById('experience').value,
        equipment: equipment,
        days_per_week: parseInt(document.getElementById('daysPerWeek').value),
        session_duration: parseInt(document.getElementById('sessionDuration').value)
    };

    showLoading(true);

    try {
        const response = await fetch(`${API_BASE_URL}/suggest-workout`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        if (!response.ok) {
            throw new Error('Failed to generate workout plan');
        }

        const data = await response.json();
        displayWorkoutResults(data);

    } catch (error) {
        console.error('Error:', error);
        alert('Error generating workout plan. Please make sure the backend server is running.');
    } finally {
        showLoading(false);
    }
}

function displayWorkoutResults(data) {
    // Show results card
    workoutResults.classList.remove('hidden');

    // Update plan info
    document.getElementById('splitName').textContent = data.split.name;
    document.getElementById('planGoal').textContent = formatGoalName(data.parameters.goal);

    // Generate workout days
    const workoutPlan = document.getElementById('workoutPlan');
    workoutPlan.innerHTML = '';

    data.workouts.forEach(workout => {
        const dayElement = createWorkoutDay(workout);
        workoutPlan.appendChild(dayElement);
    });

    // Display progression info
    displayProgression(data.progression);

    // Scroll to results
    workoutResults.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function createWorkoutDay(workout) {
    const dayDiv = document.createElement('div');
    dayDiv.className = 'workout-day';

    const dayTitle = document.createElement('h4');
    dayTitle.textContent = workout.day;
    dayDiv.appendChild(dayTitle);

    const exerciseList = document.createElement('div');
    exerciseList.className = 'exercise-list';

    workout.exercises.forEach(ex => {
        const exerciseItem = createExerciseItem(ex);
        exerciseList.appendChild(exerciseItem);
    });

    dayDiv.appendChild(exerciseList);
    return dayDiv;
}

function createExerciseItem(exercise) {
    const itemDiv = document.createElement('div');
    itemDiv.className = 'exercise-item';

    const infoDiv = document.createElement('div');
    infoDiv.className = 'exercise-info';

    const name = document.createElement('h5');
    name.textContent = exercise.exercise.name;

    const meta = document.createElement('div');
    meta.className = 'exercise-meta';
    meta.textContent = `${exercise.exercise.muscle_group.charAt(0).toUpperCase() + exercise.exercise.muscle_group.slice(1)} • ${exercise.exercise.type}`;

    infoDiv.appendChild(name);
    infoDiv.appendChild(meta);

    const volumeDiv = document.createElement('div');
    volumeDiv.className = 'exercise-volume';

    const volumeText = document.createElement('div');
    volumeText.className = 'volume-text';
    volumeText.textContent = `${exercise.sets} × ${exercise.reps}`;

    const restText = document.createElement('div');
    restText.className = 'rest-text';
    restText.textContent = `${exercise.rest_seconds}s rest`;

    volumeDiv.appendChild(volumeText);
    volumeDiv.appendChild(restText);

    itemDiv.appendChild(infoDiv);
    itemDiv.appendChild(volumeDiv);

    return itemDiv;
}

function displayProgression(progression) {
    const progressionInfo = document.getElementById('progressionInfo');
    progressionInfo.innerHTML = '';

    // Method
    const methodDiv = document.createElement('div');
    methodDiv.className = 'progression-item';
    methodDiv.innerHTML = `
        <span class="progression-label">Method:</span>
        <span class="progression-value">${progression.method}</span>
    `;
    progressionInfo.appendChild(methodDiv);

    // Increment
    const incrementDiv = document.createElement('div');
    incrementDiv.className = 'progression-item';
    incrementDiv.innerHTML = `
        <span class="progression-label">How to Progress:</span>
        <span class="progression-value">${progression.increment}</span>
    `;
    progressionInfo.appendChild(incrementDiv);

    // Deload
    const deloadDiv = document.createElement('div');
    deloadDiv.className = 'progression-item';
    deloadDiv.innerHTML = `
        <span class="progression-label">Deload Strategy:</span>
        <span class="progression-value">${progression.deload}</span>
    `;
    progressionInfo.appendChild(deloadDiv);

    // Tips
    if (progression.tips && progression.tips.length > 0) {
        const tipsDiv = document.createElement('div');
        tipsDiv.className = 'progression-tips';

        const tipsTitle = document.createElement('h5');
        tipsTitle.textContent = 'Key Tips:';
        tipsDiv.appendChild(tipsTitle);

        const tipsList = document.createElement('ul');
        progression.tips.forEach(tip => {
            const li = document.createElement('li');
            li.textContent = tip;
            tipsList.appendChild(li);
        });

        tipsDiv.appendChild(tipsList);
        progressionInfo.appendChild(tipsDiv);
    }
}

function formatGoalName(goal) {
    const goalNames = {
        'strength': 'Strength',
        'hypertrophy': 'Hypertrophy',
        'endurance': 'Endurance',
        'weight_loss': 'Weight Loss'
    };
    return goalNames[goal] || goal;
}

function showLoading(show) {
    if (show) {
        loadingOverlay.classList.remove('hidden');
    } else {
        loadingOverlay.classList.add('hidden');
    }
}

// Error handling for network issues
window.addEventListener('online', () => {
    console.log('Connection restored');
});

window.addEventListener('offline', () => {
    alert('No internet connection. Please check your connection and try again.');
});
