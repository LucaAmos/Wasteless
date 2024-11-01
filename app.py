import streamlit as st

# Initialisiere die Mitbewohner und Rechnungen
if 'roommates' not in st.session_state:
    st.session_state.roommates = []
if 'bills' not in st.session_state:
    st.session_state.bills = []

def add_roommate(name):
    # Füge einen neuen Mitbewohner hinzu
    st.session_state.roommates.append({'name': name, 'balance': 0})

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

# Titel und Beschreibung
st.title("💸 Mitbewohner Abrechnung")
st.markdown("Verwalte die gemeinsamen Ausgaben und behalte den Überblick über die Salden deiner Mitbewohner.")

# Abschnitt: Mitbewohner hinzufügen
st.subheader("👥 Mitbewohner hinzufügen")
with st.form(key='add_roommate_form'):
    new_roommate = st.text_input("Name des Mitbewohners:")
    submit_button = st.form_submit_button("Hinzufügen")
    if submit_button:
        if new_roommate:
            add_roommate(new_roommate)
            st.success(f"{new_roommate} wurde hinzugefügt!")
        else:
            st.error("Bitte einen Namen eingeben.")

# Abschnitt: Rechnung hinzufügen
st.subheader("🧾 Rechnung hinzufügen")
with st.form(key='add_bill_form'):
    amount = st.number_input("Betrag:", min_value=0.0, step=0.01, format="%.2f")
    payer = st.selectbox("Zahler:", [r['name'] for r in st.session_state.roommates])
    shared_with = st.multiselect("Geteilt mit:", [r['name'] for r in st.session_state.roommates if r['name'] != payer])

    if st.form_submit_button("Rechnung hinzufügen"):
        if amount > 0 and shared_with:
            add_bill(amount, payer, shared_with)
            st.success("Rechnung wurde hinzugefügt!")
        else:
            st.error("Bitte einen Betrag und mindestens einen Mitbewohner auswählen.")

# Abschnitt: Abrechnung anzeigen
st.subheader("📊 Aktuelle Abrechnung")
if st.session_state.roommates:
    for roommate in st.session_state.roommates:
        st.write(f"**{roommate['name']}**: {roommate['balance']:.2f} CHF")
else:
    st.info("Noch keine Mitbewohner hinzugefügt.")

# Hinweis zu den Funktionen
st.caption("🚀 Tipp: Nutze die Buttons und Eingabefelder, um Mitbewohner und Rechnungen hinzuzufügen.")
