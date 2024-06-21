from flask import Flask, request, jsonify, render_template
import os
import openai
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')


@app.route('/')
def index():
    return render_template('index.html')

def generate_recipe(weight, age, gender, exercise, goal, meal_type):
    prompt = (f"Generate a {meal_type} recipe for a {age}-year-old {gender} who weighs {weight} lbs, "
              f"exercises {exercise} times a week, and is aiming for {goal.replace('_', ' ')}. "
              f"Include ingredients, instructions, and nutrition information.")
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt}
        ]
    )
    
    result = response['choices'][0]['message']['content'].strip()
    
    parts = result.split("\n\n")
    

    title_and_ingredients = parts[0].split("\n")
    title = title_and_ingredients[0].strip()
    ingredients = None
    instructions = None
    nutrition = None
    
    for part in parts:
        if part.startswith("Ingredients:"):
            ingredients = part.replace("Ingredients:", "").strip()
        elif part.startswith("Instructions:"):
            instructions = part.replace("Instructions:", "").strip()
        elif part.startswith("Nutrition Information:"):
            nutrition = part.replace("Nutrition Information:", "").strip()
    
    if not title:
        return {"error": "Title not found in the response from OpenAI"}
    
    return {
        "title": title,
        "ingredients": ingredients,
        "instructions": instructions,
        "nutrition": nutrition
    }


@app.route('/generate-recipe', methods=['POST'])
def generate_recipe_endpoint():
    data = request.json
    weight = data.get('weight')
    age = data.get('age')
    gender = data.get('gender')
    exercise = data.get('exercise')
    goal = data.get('goal')
    meal_type = data.get('mealType')

    if not all([weight, age, gender, exercise, goal, meal_type]):
        return jsonify({"error": "All fields are required."}), 400

    try:
        recipe = generate_recipe(weight, age, gender, exercise, goal, meal_type)
        return jsonify(recipe)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
