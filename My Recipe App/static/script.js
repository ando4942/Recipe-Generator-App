document.getElementById('recipe-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const weight = document.getElementById('weight').value;
    const age = document.getElementById('age').value;
    const gender = document.getElementById('gender').value;
    const exercise = document.getElementById('exercise').value;
    const goal = document.getElementById('goal').value;
    const mealType = document.getElementById('mealType').value;

    const response = await fetch('/generate-recipe', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            weight, age, gender, exercise, goal, mealType
        })
    });

    const result = await response.json();

    if (response.ok) {
        document.getElementById('recipe-output').innerHTML = `
           <h2>${result.title}</h2>
            <h3>Ingredients:</h3>
            <p>${result.ingredients}</p>
            <h3>Instructions:</h3>
            <p>${result.instructions}</p>
            <h3>Nutrition Information:</h3>
            <p>${result.nutrition}</p>
        `;
    } else {
        document.getElementById('recipe-output').innerHTML = `<p>Error: ${result.error}</p>`;
    }
});
