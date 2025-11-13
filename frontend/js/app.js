// API Configuration
const API_BASE_URL = 'http://localhost:5000/api';

// Current unit system
let currentUnit = 'metric';

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    showSection('home');
});

function setupEventListeners() {
    // Unit toggle
    document.querySelectorAll('.toggle-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            switchUnits(btn.dataset.unit);
        });
    });

    // Auto-round inputs
    document.querySelectorAll('input[type="number"]').forEach(input => {
        input.addEventListener('blur', autoRound);
    });

    // Form submissions
    document.getElementById('calorieForm').addEventListener('submit', handleCalorieSubmit);
    document.getElementById('workoutForm').addEventListener('submit', handleWorkoutSubmit);
}

function showSection(section) {
    // Hide all sections
    document.querySelectorAll('.section').forEach(s => s.classList.add('hidden'));

    // Show requested section
    if (section === 'home') {
        document.querySelector('.hero').scrollIntoView({ behavior: 'smooth' });
    } else {
        document.getElementById(section).classList.remove('hidden');
        document.getElementById(section).scrollIntoView({ behavior: 'smooth' });
    }
}

function switchUnits(unit) {
    currentUnit = unit;

    // Update toggle buttons
    document.querySelectorAll('.toggle-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.unit === unit);
    });

    // Show/hide appropriate inputs
    if (unit === 'metric') {
        document.getElementById('metricInputs').classList.remove('hidden');
        document.getElementById('imperialInputs').classList.add('hidden');

        // Clear imperial and set metric required
        document.getElementById('heightFt').removeAttribute('required');
        document.getElementById('heightIn').removeAttribute('required');
        document.getElementById('weightLbs').removeAttribute('required');
        document.getElementById('heightCm').setAttribute('required', 'required');
        document.getElementById('weightKg').setAttribute('required', 'required');
    } else {
        document.getElementById('metricInputs').classList.add('hidden');
        document.getElementById('imperialInputs').classList.remove('hidden');

        // Clear metric and set imperial required
        document.getElementById('heightCm').removeAttribute('required');
        document.getElementById('weightKg').removeAttribute('required');
        document.getElementById('heightFt').setAttribute('required', 'required');
        document.getElementById('heightIn').setAttribute('required', 'required');
        document.getElementById('weightLbs').setAttribute('required', 'required');
    }
}

function autoRound(e) {
    const input = e.target;
    if (input.value) {
        // Round to 1 decimal place
        input.value = Math.round(parseFloat(input.value) * 10) / 10;
    }
}

// Unit Conversions
function lbsToKg(lbs) {
    return lbs * 0.453592;
}

function feetInchesToCm(feet, inches) {
    const totalInches = (feet * 12) + inches;
    return totalInches * 2.54;
}

// Calorie Calculator
async function handleCalorieSubmit(e) {
    e.preventDefault();

    // Get form data
    const age = parseInt(document.getElementById('age').value);
    const gender = document.getElementById('gender').value;
    const activity = document.getElementById('activity').value;
    const goal = document.getElementById('goal').value;

    let height, weight;

    // Convert units if needed
    if (currentUnit === 'metric') {
        height = parseFloat(document.getElementById('heightCm').value);
        weight = parseFloat(document.getElementById('weightKg').value);
    } else {
        const feet = parseInt(document.getElementById('heightFt').value);
        const inches = parseInt(document.getElementById('heightIn').value);
        const lbs = parseFloat(document.getElementById('weightLbs').value);

        height = Math.round(feetInchesToCm(feet, inches));
        weight = Math.round(lbsToKg(lbs) * 10) / 10;
    }

    const formData = {
        age,
        height,
        weight,
        gender,
        activity_level: activity,
        goal
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
    // Show results
    document.getElementById('calorieResults').classList.remove('hidden');

    // Update values
    document.getElementById('bmr').textContent = `${data.bmr} kcal`;
    document.getElementById('tdee').textContent = `${data.tdee} kcal`;
    document.getElementById('targetCalories').textContent = `${data.target_calories} kcal`;

    // Update macros
    const macros = data.macros;
    document.getElementById('proteinValue').textContent = `${macros.protein.grams}g`;
    document.getElementById('carbsValue').textContent = `${macros.carbs.grams}g`;
    document.getElementById('fatsValue').textContent = `${macros.fats.grams}g`;

    // Update recommendations
    const recList = document.getElementById('recommendationsList');
    recList.innerHTML = '';
    data.recommendations.forEach(rec => {
        const li = document.createElement('li');
        li.textContent = rec;
        recList.appendChild(li);
    });

    // Scroll to results
    document.getElementById('calorieResults').scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Workout Suggester
async function handleWorkoutSubmit(e) {
    e.preventDefault();

    const equipmentCheckboxes = document.querySelectorAll('input[name="equipment"]:checked');
    const equipment = Array.from(equipmentCheckboxes).map(cb => cb.value);

    if (equipment.length === 0) {
        alert('Please select at least one equipment option');
        return;
    }

    const formData = {
        gender: document.getElementById('workoutGender').value,
        goal: document.getElementById('workoutGoal').value,
        experience: document.getElementById('experience').value,
        equipment: equipment,
        days_per_week: parseInt(document.getElementById('daysPerWeek').value),
        session_duration: 60
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
    document.getElementById('workoutResults').classList.remove('hidden');

    document.getElementById('splitName').textContent = data.split.name;
    document.getElementById('planGoal').textContent = formatGoalName(data.parameters.goal);

    const workoutPlan = document.getElementById('workoutPlan');
    workoutPlan.innerHTML = '';

    data.workouts.forEach(workout => {
        const dayElement = createWorkoutDay(workout);
        workoutPlan.appendChild(dayElement);
    });

    displayProgression(data.progression);

    document.getElementById('workoutResults').scrollIntoView({ behavior: 'smooth', block: 'nearest' });
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

    // Format subcategory for display
    let subcategoryText = '';
    if (exercise.exercise.subcategory) {
        subcategoryText = formatSubcategory(exercise.exercise.subcategory);
    }

    const muscleGroup = exercise.exercise.muscle_group.charAt(0).toUpperCase() + exercise.exercise.muscle_group.slice(1);
    let metaHTML = subcategoryText ? `${muscleGroup} - ${subcategoryText}` : muscleGroup;

    // Add secondary muscles if available
    if (exercise.exercise.secondary_muscles && exercise.exercise.secondary_muscles.length > 0) {
        const secondaryText = exercise.exercise.secondary_muscles.join(', ');
        metaHTML += `<br><span class="secondary-muscles">+ ${secondaryText}</span>`;
    }

    meta.innerHTML = metaHTML;

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

    // Always add view form button (show for all exercises now)
    const viewButton = document.createElement('button');
    viewButton.className = 'view-form-btn';
    viewButton.textContent = 'View Form';
    viewButton.onclick = (e) => {
        e.stopPropagation();
        showExerciseDetails(exercise.exercise);
    };
    itemDiv.appendChild(viewButton);

    return itemDiv;
}

function formatSubcategory(subcategory) {
    // Convert underscore format to readable text
    return subcategory
        .split('_')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ');
}

function showExerciseDetails(exercise) {
    const modal = document.getElementById('exerciseModal');
    const modalTitle = document.getElementById('modalExerciseName');
    const modalSubcategory = document.getElementById('modalSubcategory');
    const modalSecondary = document.getElementById('modalSecondaryMuscles');
    const modalDescription = document.getElementById('modalDescription');
    const startImg = document.getElementById('startPositionImg');
    const endImg = document.getElementById('endPositionImg');

    modalTitle.textContent = exercise.name;

    // Show subcategory if available
    if (exercise.subcategory) {
        modalSubcategory.textContent = formatSubcategory(exercise.subcategory);
        modalSubcategory.classList.remove('hidden');
    } else {
        modalSubcategory.classList.add('hidden');
    }

    // Show secondary muscles if available
    if (exercise.secondary_muscles && exercise.secondary_muscles.length > 0) {
        modalSecondary.textContent = 'Also works: ' + exercise.secondary_muscles.join(', ');
        modalSecondary.classList.remove('hidden');
    } else {
        modalSecondary.classList.add('hidden');
    }

    // Show description
    if (exercise.description) {
        modalDescription.textContent = exercise.description;
        modalDescription.classList.remove('hidden');
    } else {
        modalDescription.classList.add('hidden');
    }

    // Show images if available
    if (exercise.start_image && exercise.end_image) {
        startImg.src = exercise.start_image;
        startImg.alt = `${exercise.name} - Start Position`;
        endImg.src = exercise.end_image;
        endImg.alt = `${exercise.name} - End Position`;
    }

    modal.classList.remove('hidden');
}

function closeExerciseModal() {
    document.getElementById('exerciseModal').classList.add('hidden');
}

function displayProgression(progression) {
    const progressionInfo = document.getElementById('progressionInfo');
    progressionInfo.innerHTML = '';

    const methodDiv = document.createElement('div');
    methodDiv.className = 'progression-item';
    methodDiv.innerHTML = `
        <strong>Method:</strong> ${progression.method}<br>
        <strong>How to Progress:</strong> ${progression.increment}<br>
        <strong>Deload:</strong> ${progression.deload}
    `;
    progressionInfo.appendChild(methodDiv);

    if (progression.tips && progression.tips.length > 0) {
        const tipsList = document.createElement('ul');
        progression.tips.forEach(tip => {
            const li = document.createElement('li');
            li.textContent = tip;
            tipsList.appendChild(li);
        });
        progressionInfo.appendChild(tipsList);
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
        document.getElementById('loading').classList.remove('hidden');
    } else {
        document.getElementById('loading').classList.add('hidden');
    }
}
