import streamlit as st
import requests

# Setze deinen Spoonacular API-Schlüssel hier ein
api_key = '21c590f808c74caabbaa1494c6196e7a'

# Titel der App
st.title("Wasteless")

# Eingabefeld für die Zutaten
ingredients = st.text_input("Gib die Zutaten ein (getrennt durch Kommas, z.B.: tomate, käse, basilikum):")

# Button zum Suchen der Rezepte
if st.button("Rezepte finden"):
    if ingredients:
        # URL für die API-Anfrage
        url = f"https://api.spoonacular.com/recipes/findByIngredients?ingredients={ingredients}&number=5&apiKey={api_key}"
        
        # Anfrage an die Spoonacular API
        response = requests.get(url)
        
        # Überprüfen, ob die Anfrage erfolgreich war
        if response.status_code == 200:
            recipes = response.json()
            
            # Wenn Rezepte gefunden wurden, zeigen wir sie an
            if recipes:
                st.write(f"Rezepte für die Zutaten: {ingredients}")
                for recipe in recipes:
                    st.subheader(recipe['title'])
                    st.image(recipe['image'], width=200)
                    st.write(f"[Rezept ansehen](https://spoonacular.com/recipes/{recipe['title'].replace(' ', '-')}-{recipe['id']})")
                    st.write("---")
            else:
                st.write("Keine Rezepte gefunden. Versuch es mit anderen Zutaten.")
        else:
            st.write("Fehler beim Abrufen der Rezepte. Bitte überprüfe den API-Schlüssel und die Internetverbindung.")
    else:
        st.write("Bitte gib mindestens eine Zutat ein.")