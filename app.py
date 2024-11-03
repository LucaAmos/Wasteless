pip install pytesseract
pip install matplotlib.pyplot

import streamlit as st
import matplotlib.pyplot as plt
import requests
from PIL import Image
import pytesseract

# Spoonacular API key
api_key = "21c590f808c74caabbaa1494c6196e7a"

# Set Streamlit page configuration
st.set_page_config(page_title='Roommate Expense and Recipe Tracker')

# Initialize roommates and bills
if 'roommates' not in st.session_state:
    st.session_state.roommates = []
if 'bills' not in st.session_state:
    st.session_state.bills = []

def add_roommate(name):
    # Add a new roommate
    st.session_state.roommates.append({'name': name, 'balance': 0, 'total_spent': 0})

def add_bill(amount, payer, shared_with):
    # Add a bill and update balances
    bill = {'amount': amount, 'payer': payer, 'shared_with': shared_with}
    st.session_state.bills.append(bill)
    update_balances(amount, payer, shared_with)

def update_balances(amount, payer, shared_with):
    # Calculate each person's share and update balances
    share_per_person = amount / (len(shared_with) + 1)  # +1 for the payer
    for roommate in shared_with:
        for r in st.session_state.roommates:
            if r['name'] == roommate:
                r['balance'] -= share_per_person
    for r in st.session_state.roommates:
        if r['name'] == payer:
            r['balance'] += amount
            r['total_spent'] += amount

# App title
st.title("Roommate Expense and Recipe Tracker")

# Add Roommates
st.header("Add Roommate")
new_roommate = st.text_input("Roommate's Name:")
if st.button("Add Roommate"):
    if new_roommate:
        add_roommate(new_roommate)
        st.success(f"{new_roommate} has been added!")
    else:
        st.error("Please enter a name.")

# Add Bills
st.header("Add Bill")
amount = st.number_input("Amount:", min_value=0.0)
payer = st.selectbox("Payer:", [r['name'] for r in st.session_state.roommates])
shared_with = st.multiselect("Shared With:", [r['name'] for r in st.session_state.roommates if r['name'] != payer])

if st.button("Add Bill"):
    if amount > 0 and shared_with:
        add_bill(amount, payer, shared_with)
        st.success("Bill added!")
    else:
        st.error("Please enter an amount and select at least one roommate.")

# Display Balances
st.header("Balances")
if st.session_state.roommates:
    for roommate in st.session_state.roommates:
        st.write(f"{roommate['name']}: {roommate['balance']:.2f} CHF")
else:
    st.write("No roommates added.")

# Display Expense Overview
st.header("Expense Overview")
if st.session_state.roommates:
    # Names and total spent for each roommate for the pie chart
    names = [r['name'] for r in st.session_state.roommates]
    total_spent = [r['total_spent'] for r in st.session_state.roommates]
    
    if sum(total_spent) > 0:  # Show pie chart only if there are expenses
        fig, ax = plt.subplots()
        ax.pie(total_spent, labels=names, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # Equal aspect ratio to make pie chart a circle
        st.pyplot(fig)
    else:
        st.write("No expenses recorded yet.")

# Recipe Finder Section
st.header("Find Recipes Based on Ingredients")
ingredients = st.text_input("Enter ingredients you have (comma-separated)", "tomato,cheese,basil")

if st.button("Find Recipes"):
    url = f"https://api.spoonacular.com/recipes/findByIngredients?ingredients={ingredients}&number=10&apiKey={api_key}"
    response = requests.get(url)
    
    if response.status_code == 200:
        recipes = response.json()
        perfect_matches = []
        almost_matches = []
        
        for recipe in recipes:
            missing_ingredients = recipe['missedIngredientCount']
            if missing_ingredients == 0:
                perfect_matches.append(recipe)
            else:
                almost_matches.append(recipe)
        
        st.subheader("Recipes you can make with all ingredients:")
        for recipe in perfect_matches:
            st.write(f"**{recipe['title']}**")
            st.write(f"[Link to recipe](https://spoonacular.com/recipes/{recipe['title'].replace(' ', '-')}-{recipe['id']})")
        
        st.subheader("Recipes you could make, missing some ingredients:")
        for recipe in almost_matches:
            missing = [ingredient['name'] for ingredient in recipe['missedIngredients']]
            st.write(f"**{recipe['title']}**")
            st.write(f"Missing ingredients: {', '.join(missing)}")
            st.write(f"[Link to recipe](https://spoonacular.com/recipes/{recipe['title'].replace(' ', '-')}-{recipe['id']})")
    else:
        st.error(f"Error: {response.status_code}")

# Receipt Upload and OCR Section
st.header("Upload and Scan Receipt for Expenses")
datafile = st.file_uploader("Upload your receipt", type=["png", "jpg", "jpeg"])

if datafile is not None:
    image = Image.open(datafile)
    st.image(image, caption="Uploaded Receipt", use_column_width=True)
    st.write("Extracting text from the receipt...")
    
    # OCR processing
    text = pytesseract.image_to_string(image)
    st.text_area("Extracted Text", text, height=250)
