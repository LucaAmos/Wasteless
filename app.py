import streamlit as st
import requests

# Setze deinen Spoonacular API-Schlüssel hier ein
api_key = '21c590f808c74caabbaa1494c6196e7a'

# Titel der App
st.title("WasteLess")

# List of ingredients you have, separated by commas (e.g., "apples,flour,sugar")
ingredients = "tomato,cheese,basil"

# URL to search for recipes that can be made with only the available ingredients
url = f"https://api.spoonacular.com/recipes/findByIngredients?ingredients={ingredients}&number=10&apiKey={api_key}"

# Send HTTP GET request
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    recipes = response.json()
    perfect_matches = []
    almost_matches = []

    for recipe in recipes:
        # Count of missing ingredients for each recipe
        missing_ingredients = recipe['missedIngredientCount']
        
        if missing_ingredients == 0:
            # Recipes with all ingredients available
            perfect_matches.append(recipe)
        else:
            # Recipes that need additional ingredients
            almost_matches.append(recipe)
    
    # Display recipes with all ingredients
    print("Recipes you can make with all ingredients you have:")
    for recipe in perfect_matches:
        print(f"- {recipe['title']}")
        print(f"  Link: https://spoonacular.com/recipes/{recipe['title'].replace(' ', '-')}-{recipe['id']}\n")

    # Display recipes that need additional ingredients
    print("Recipes you could make, but you're missing some ingredients:")
    for recipe in almost_matches:
        missing = [ingredient['name'] for ingredient in recipe['missedIngredients']]
        print(f"- {recipe['title']}")
        print(f"  Missing ingredients: {', '.join(missing)}")
        print(f"  Link: https://spoonacular.com/recipes/{recipe['title'].replace(' ', '-')}-{recipe['id']}\n")
else:
    print(f"Error: {response.status_code}")