import streamlit as st
import requests

# API-Key für Spoonacular
API_KEY = '21c590f808c74caabbaa1494c6196e7a'
SPOONACULAR_URL = 'https://api.spoonacular.com/recipes/findByIngredients'

# Initialisiere die Mitbewohner und Rechnungen
if 'roommates' not in st.session_state:
    st.session_state.roommates = []
if 'bills' not in st.session_state:
    st.session_state.bills = []

def add_roommate(name):
    st.session_state.roommates.append({'name': name, 'balance': 0, 'total_spent': 0})

def add_bill(amount, payer, shared_with):
    bill = {'amount': amount, 'payer': payer, 'shared_with': shared_with}
    st.session_state.bills.append(bill)
    update_balances(amount, payer, shared_with)

def update_balances(amount, payer, shared_with):
    share_per_person = amount / (len(shared_with) + 1)
    for roommate in shared_with:
        for r in st.session_state.roommates:
            if r['name'] == roommate:
                r['balance'] -= share_per_person
    for r in st.session_state.roommates:
        if r['name'] == payer:
            r['balance'] += amount
            r['total_spent'] += amount

def get_recipes(ingredients):
    params = {
        'ingredients': ','.join(ingredients),
        'number': 5,
        'apiKey': API_KEY
    }
    response = requests.get(SPOONACULAR_URL, params=params)
    return response.json() if response.status_code == 200 else []

st.title("Wasteless App")

# Zutaten eingeben
st.header("Zutaten eingeben")
ingredients_input = st.text_input("Gib deine Zutaten ein (kommagetrennt):")
if st.button("Rezepte suchen"):
    ingredients = [ingredient.strip() for ingredient in ingredients_input.split(',')]
    recipes = get_recipes(ingredients)
    
    if recipes:
        st.subheader("Gefundene Rezepte:")
        for recipe in recipes:
            st.write(f"- {recipe['title']}")
    else:
        st.write("Keine Rezepte gefunden mit diesen Zutaten.")

# Mitbewohner hinzufügen
st.header("Mitbewohner hinzufügen")
new_roommate = st.text_input("Name des Mitbewohners:")
if st.button("Hinzufügen"):
    if new_roommate:
        add_roommate(new_roommate)
        st.success(f"{new_roommate} wurde hinzugefügt!")

# Rechnungen hinzufügen
st.header("Rechnung hinzufügen")
amount = st.number_input("Betrag:", min_value=0.0)
payer = st.selectbox("Zahler:", [r['name'] for r in st.session_state.roommates])
shared_with = st.multiselect("Geteilt mit:", [r['name'] for r in st.session_state.roommates if r['name'] != payer])

if st.button("Rechnung hinzufügen"):
    if amount > 0 and shared_with:
        add_bill(amount, payer, shared_with)
        st.success("Rechnung hinzugefügt!")

# Abrechnung anzeigen
st.header("Abrechnung")
if st.session_state.roommates:
    for roommate in st.session_state.roommates:
        st.write(f"{roommate['name']}: {roommate['balance']:.2f} CHF")
else:
    st.write("Keine Mitbewohner hinzugefügt.")

# Datei-Upload für Rechnungen
datafile = st.file_uploader(label='Upload your receipt')

if datafile is not None:
    st.success("Rechnung hochgeladen!")
