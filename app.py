import streamlit as st
import matplotlib.pyplot as plt

# Initialisiere die Mitbewohner und Rechnungen
if 'roommates' not in st.session_state:
    st.session_state.roommates = []
if 'bills' not in st.session_state:
    st.session_state.bills = []

def add_roommate(name):
    # Füge einen neuen Mitbewohner hinzu
    st.session_state.roommates.append({'name': name, 'balance': 0, 'total_spent': 0})

def add_bill(amount, payer, shared_with):
    # Füge eine Rechnung hinzu und aktualisiere die Salden
    bill = {'amount': amount, 'payer': payer, 'shared_with': shared_with}
    st.session_state.bills.append(bill)
    update_balances(amount, payer, shared_with)

def update_balances(amount, payer, shared_with):
    # Berechne den Anteil pro Person und aktualisiere die Salden der Mitbewohner
    share_per_person = amount / (len(shared_with) + 1)  # +1 für den Zahler
    for roommate in shared_with:
        for r in st.session_state.roommates:
            if r['name'] == roommate:
                r['balance'] -= share_per_person
    for r in st.session_state.roommates:
        if r['name'] == payer:
            r['balance'] += amount
            r['total_spent'] += amount  # Aktualisiere die Gesamtausgaben des Zahlers

st.title("Mitbewohner Abrechnung")

# Mitbewohner hinzufügen
st.header("Mitbewohner hinzufügen")
new_roommate = st.text_input("Name des Mitbewohners:")
if st.button("Hinzufügen"):
    if new_roommate:
        add_roommate(new_roommate)
        st.success(f"{new_roommate} wurde hinzugefügt!")
    else:
        st.error("Bitte einen Namen eingeben.")

# Rechnungen hinzufügen
st.header("Rechnung hinzufügen")
amount = st.number_input("Betrag:", min_value=0.0)
payer = st.selectbox("Zahler:", [r['name'] for r in st.session_state.roommates])
shared_with = st.multiselect("Geteilt mit:", [r['name'] for r in st.session_state.roommates if r['name'] != payer])

if st.button("Rechnung hinzufügen"):
    if amount > 0 and shared_with:
        add_bill(amount, payer, shared_with)
        st.success("Rechnung hinzugefügt!")
    else:
        st.error("Bitte einen Betrag und mindestens einen Mitbewohner auswählen.")

# Abrechnung anzeigen
st.header("Abrechnung")
if st.session_state.roommates:
    for roommate in st.session_state.roommates:
        st.write(f"{roommate['name']}: {roommate['balance']:.2f} CHF")
else:
    st.write("Keine Mitbewohner hinzugefügt.")

# Grafische Darstellung der Ausgaben
st.header("Ausgabenübersicht")

if st.session_state.roommates:
    # Namen und Ausgaben der Mitbewohner für das Kuchendiagramm extrahieren
    names = [r['name'] for r in st.session_state.roommates]
    total_spent = [r['total_spent'] for r in st.session_state.roommates]
    
    if sum(total_spent) > 0:  # Nur anzeigen, wenn Ausgaben vorhanden sind
        fig, ax = plt.subplots()
        ax.pie(total_spent, labels=names, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # Kreisdiagramm kreisförmig darstellen
        st.pyplot(fig)
    else:
        st.write("Es wurden noch keine Ausgaben erfasst.")

