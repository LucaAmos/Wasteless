import streamlit as st
import requests

# Function to fetch recipes from the Spoonacular API
def fetch_recipes(ingredients):
    api_key = "21c590f808c74caabbaa1494c6196e7a"
    url = f"https://api.spoonacular.com/recipes/findByIngredients?ingredients={','.join(ingredients)}&apiKey={api_key}"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else []

# App title
st.title("WasteLess")

# Set WG name
wg_name = st.text_input("Enter the name of your shared apartment:")
if wg_name:
    st.session_state.wg_name = wg_name
    st.success(f"Welcome to the shared apartment: {wg_name}")

    # Add roommates
    if "roommates" not in st.session_state:
        st.session_state.roommates = []

    roommate_name = st.text_input("Add a roommate:")
    if st.button("Add Roommate"):
        if roommate_name and roommate_name not in st.session_state.roommates:
            st.session_state.roommates.append(roommate_name)
            st.success(f"{roommate_name} has been added.")
        elif roommate_name in st.session_state.roommates:
            st.warning(f"{roommate_name} is already on the list.")

    st.write("Roommates:")
    for roommate in st.session_state.roommates:
        st.write(f"- {roommate}")

    # Add inventory
    if "inventory" not in st.session_state:
        st.session_state.inventory = []

    item_name = st.text_input("Enter the name of the item:")
    buyer_name = st.selectbox("Who bought it?", [""] + st.session_state.roommates)
    amount_spent = st.number_input("How much was spent?", min_value=0.0, format="%.2f")
    
    if st.button("Add Item"):
        if item_name and buyer_name:
            st.session_state.inventory.append({
                "item": item_name,
                "buyer": buyer_name,
                "amount": amount_spent
            })
            st.success(f"{item_name} has been added to the inventory.")
        else:
            st.warning("Please enter an item name and select a buyer.")

    st.write("Inventory:")
    for item in st.session_state.inventory:
        st.write(f"- {item['item']} (Bought by: {item['buyer']}, Amount: {item['amount']:.2f})")

    # Suggest recipes
    if st.session_state.inventory:
        ingredients = [item["item"] for item in st.session_state.inventory]
        recipes = fetch_recipes(ingredients)

        if recipes:
            st.write("Suggested Recipes:")
            for recipe in recipes:
                st.write(f"- {recipe['title']}")
        else:
            st.warning("No recipes found.")
else:
    st.warning("Please enter a shared apartment name to continue.")

