import streamlit as st
import random

# Emoji-Liste für WG-Name
emoji_list = ["🏠", "🏡", "👫", "👬", "👭", "👯", "💸"]
random_emoji = random.choice(emoji_list)

# Caching-Funktion zur Emoji-Auswahl
@st.cache
def get_auto_emoji(description):
    if "essen" in description.lower() or "lebensmittel" in description.lower():
        return "🍕"
    elif "miete" in description.lower():
        return "🏡"
    elif "internet" in description.lower():
        return "🌐"
    elif "strom" in description.lower() or "energie" in description.lower():
        return "💡"
    else:
        return "💸"  # Standard-Emoji für sonstige Ausgaben

# WG Name und Initialisierung für Mitbewohner und Rechnungen
st.title("WG Kostenverwaltung")
if 'wg_name' not in st.session_state:
    st.session_state.wg_name = "Meine WG"

st.session_state.setdefault('roommates', [])
st.session_state.setdefault('bills', [])

# Live-Update des WG-Namens
wg_name_input = st.text_input("WG Name", value=st.session_state.wg_name)
st.session_state.wg_name = wg_name_input
st.markdown(f"<h1 style='text-align: center; font-size: 50px;'>{wg_name_input} {random_emoji}</h1>", unsafe_allow_html=True)

def add_roommate(name):
    # Füge einen neuen Mitbewohner hinzu, falls nicht schon vorhanden
    if name not in [r['name'] for r in st.session_state.roommates]:
        st.session_state.roommates.append({'name': name, 'balance': 0})

def add_bill(amount, payer, shared_with, description):
    # Emoji für Rechnung automatisch basieren auf Beschreibung auswählen
    emoji = get_auto_emoji(description)
    bill = {'amount': amount, 'payer': payer, 'shared_with': shared_with, 'description': description, 'emoji': emoji}
    st.session_state.bills.append(bill)
    update_balances(amount, payer, shared_with)

def update_balances(amount, payer, shared_with):
    # Berechne den Anteil pro Person und aktualisiere die Salden der Mitbewohner
    share_per_person = amount / (len(shared_with) + 1)
    for roommate in shared_with:
        for r in st.session_state.roommates:
            if r['name'] == roommate:
                r['balance'] -= share_per_person
    for r in st.session_state.roommates:
        if r['name'] == payer:
            r['balance'] += amount

# Sidebar zur schnellen Übersicht
with st.sidebar:
    st.subheader("👥 Bewohner und Salden")
    if st.session_state.roommates:
        for roommate in st.session_state.roommates:
            balance_color = "green" if roommate['balance'] >= 0 else "red"
            st.markdown(f"<span style='color:{balance_color}; font-weight:bold;'>{roommate['name']}: {roommate['balance']:.2f} CHF</span>", unsafe_allow_html=True)
    else:
        st.info("Noch keine Mitbewohner hinzugefügt.")

# Abschnitt: Mitbewohner hinzufügen
st.subheader("Mitbewohner hinzufügen")
with st.form(key='add_roommate_form'):
    new_roommate = st.text_input("Name des Mitbewohners:")
    submit_button = st.form_submit_button("Hinzufügen")
    if submit_button and new_roommate:
        add_roommate(new_roommate)
        st.success(f"{new_roommate} wurde hinzugefügt!")

# Abschnitt: Rechnung hinzufügen
st.subheader("Rechnung hinzufügen")
with st.form(key='add_bill_form'):
    amount = st.number_input("Betrag:", min_value=0.0, step=0.01, format="%.2f")
    payer = st.selectbox("Zahler:", [r['name'] for r in st.session_state.roommates], help="Wer hat die Rechnung bezahlt?")
    shared_with = st.multiselect("Geteilt mit:", [r['name'] for r in st.session_state.roommates if r['name'] != payer], help="Mit wem wurde die Ausgabe geteilt?")
    description = st.text_input("Beschreibung der Ausgabe (z.B. Lebensmittel, Miete)")

    if st.form_submit_button("Rechnung hinzufügen") and amount > 0 and shared_with and description:
        add_bill(amount, payer, shared_with, description)
        st.success("Rechnung wurde hinzugefügt!")

# Abschnitt: Abrechnung anzeigen
st.subheader("Aktuelle Abrechnung")
if st.session_state.bills:
    for bill in st.session_state.bills:
        st.write(f"{bill['emoji']} **{bill['description']}** - {bill['amount']:.2f} CHF, bezahlt von {bill['payer']}, geteilt mit {', '.join(bill['shared_with'])}")
else:
    st.info("Noch keine Rechnungen hinzugefügt.")

