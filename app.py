import streamlit as st

# Initialisiere die WG-Informationen
if 'wg_name' not in st.session_state:
    st.session_state.wg_name = "Meine WG"
if 'roommates' not in st.session_state:
    st.session_state.roommates = []
if 'bills' not in st.session_state:
    st.session_state.bills = []

def set_wg_name(name):
    st.session_state.wg_name = name

def add_roommate(name):
    # Füge einen neuen Mitbewohner hinzu
    st.session_state.roommates.append({'name': name, 'balance': 0})

def add_bill(amount, payer, shared_with, description, emoji):
    # Füge eine Rechnung hinzu und aktualisiere die Salden
    bill = {'amount': amount, 'payer': payer, 'shared_with': shared_with, 'description': description, 'emoji': emoji}
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

# WG-Name festlegen
st.title("🏠 Mitbewohner Abrechnung")
st.markdown("Verwalte die gemeinsamen Ausgaben und behalte den Überblick über die Salden deiner Mitbewohner.")

st.subheader("WG-Name festlegen")
wg_name_input = st.text_input("Name der WG:", value=st.session_state.wg_name)
if st.button("Speichern"):
    set_wg_name(wg_name_input)
    st.success(f"WG-Name gespeichert als: {wg_name_input}")

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
    payer = st.selectbox("Zahler:", [r['name'] for r in st.session_state.roommates], help="Wer hat die Rechnung bezahlt?")
    shared_with = st.multiselect("Geteilt mit:", [r['name'] for r in st.session_state.roommates if r['name'] != payer], help="Mit wem wurde die Ausgabe geteilt?")
    description = st.text_input("Beschreibung der Ausgabe (z.B. Lebensmittel, Miete)")
    emoji = st.text_input("Emoji (z.B. 🍕, 🛒, 🏡) für die Ausgabe")
    
    if st.form_submit_button("Rechnung hinzufügen"):
        if amount > 0 and shared_with and description:
            add_bill(amount, payer, shared_with, description, emoji)
            st.success("Rechnung wurde hinzugefügt!")
        else:
            st.error("Bitte einen Betrag, eine Beschreibung und mindestens einen Mitbewohner auswählen.")

# Abschnitt: Abrechnung anzeigen
st.subheader("📊 Aktuelle Abrechnung in der WG")
st.write(f"**WG-Name:** {st.session_state.wg_name}")
if st.session_state.roommates:
    st.write("### Bewohner und Salden:")
    for roommate in st.session_state.roommates:
        balance_color = "green" if roommate['balance'] >= 0 else "red"
        st.markdown(f"<span style='color:{balance_color}; font-weight:bold;'>{roommate['name']}: {roommate['balance']:.2f} CHF</span>", unsafe_allow_html=True)
else:
    st.info("Noch keine Mitbewohner hinzugefügt.")

# Liste der Rechnungen anzeigen
if st.session_state.bills:
    st.write("### Letzte Ausgaben:")
    for bill in st.session_state.bills:
        st.write(f"{bill['emoji']} **{bill['description']}** - {bill['amount']:.2f} CHF, bezahlt von {bill['payer']}, geteilt mit {', '.join(bill['shared_with'])}")
else:
    st.info("Noch keine Rechnungen hinzugefügt.")

# Hinweis zu den Funktionen
st.caption("🚀 Tipp: Nutze die Buttons und Eingabefelder, um Mitbewohner und Rechnungen hinzuzufügen.")

