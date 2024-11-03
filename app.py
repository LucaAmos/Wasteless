import streamlit as st
import requests

# API-Key für Spoonacular
API_KEY = '21c590f808c74caabbaa1494c6196e7a'
SPOONACULAR_URL = 'https://api.spoonacular.com/recipes/findByIngredients'

# Initialisiere die WG-Daten
if 'wg_name' not in st.session_state:
    st.session_state.wg_name = ""
if 'roommates' not in st.session_state:
    st.session_state.roommates = []
if 'inventory' not in st.session_state:
    st.session_state.inventory = []

def add_roommate(name):
    st.session_state.roommates.append(name)

def add_inventory_item(item):
    st.session_state.inventory.append(item)

def get_recipes(ingredients):
    params = {
        'ingredients': ','.join(ingredients),
        'number': 5,
        'apiKey': API_KEY
    }
    response = requests.get(SPOONACULAR_URL, params=params)
    return response.json() if response.status_code == 200 else []

st.title("🏠 Wasteless App")

# WG Name eingeben
st.header("🏡 Enter Your Shared Apartment Details")
wg_name = st.text_input("Enter your WG name:")
if wg_name:
    st.session_state.wg_name = wg_name
    st.success(f"WG Name set to: {wg_name}")

# Mitbewohner hinzufügen
st.header("👥 Add Roommates")
new_roommate = st.text_input("Name of the roommate:")
if st.button("Add Roommate"):
    if new_roommate:
        add_roommate(new_roommate)
        st.success(f"{new_roommate} has been added!")

# WG Inventar hinzufügen
st.header("🛒 Add Inventory Items")
new_inventory_item = st.text_input("Add an item to the inventory:")
if st.button("Add Inventory Item"):
    if new_inventory_item:
        add_inventory_item(new_inventory_item)
        st.success(f"{new_inventory_item} has been added to the inventory!")

# Zeige die Mitbewohner und das Inventar an
st.subheader("👥 Roommates:")
if st.session_state.roommates:
    for roommate in st.session_state.roommates:
        st.write(f"- {roommate}")
else:
    st.write("No roommates added.")

st.subheader("🛒 Inventory:")
if st.session_state.inventory:
    for item in st.session_state.inventory:
        st.write(f"- {item}")
else:
    st.write("No inventory items added.")

# Rezepte suchen
st.header("🍽️ Find Recipes")
if st.button("Get Recipes"):
    if st.session_state.inventory:
        recipes = get_recipes(st.session_state.inventory)
        if recipes:
            st.subheader("Found Recipes:")
            for recipe in recipes:
                st.write(f"- {recipe['title']}")
        else:
            st.write("No recipes found with these ingredients.")
    else:
        st.warning("Please add inventory items first to find recipes.")

# Rechnung hochladen
datafile = st.file_uploader(label='📄 Upload your receipt')

if datafile is not None:
    st.success("Receipt uploaded!")
