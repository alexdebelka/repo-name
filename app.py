import streamlit as st
import json
import os
from datetime import datetime

# Define the Client and Product classes
class Client:
    def __init__(self, nume, credit, credit_initial, numar_telefon, id_unic, email):
        self.nume = nume
        self.credit = credit
        self.credit_initial = credit_initial
        self.numar_telefon = numar_telefon
        self.id_unic = id_unic
        self.email = email

class Produs:
    def __init__(self, nume, pret):
        self.nume = nume
        self.pret = pret

# File for storing data
FISIER_DATE = 'data.json'

# Functions for reading and writing data to JSON file
def incarca_date():
    if os.path.exists(FISIER_DATE):
        with open(FISIER_DATE, 'r') as f:
            date = json.load(f)
            return date
    else:
        return {'clienti': {}, 'produse': {}, 'comenzi': {}}

def salveaza_date(date):
    with open(FISIER_DATE, 'w') as f:
        json.dump(date, f)

# Load existing data
date = incarca_date()

# Ensure dictionaries for clients, products, and orders exist
if 'clienti' not in date:
    date['clienti'] = {}
if 'produse' not in date:
    date['produse'] = {}
if 'comenzi' not in date:
    date['comenzi'] = {}

# Create dictionaries for clients and products from loaded data
clienti = {
    nume: Client(nume, info['credit'], info.get('credit_initial', info['credit']), info.get('numar_telefon', ''), info.get('id_unic', ''), info.get('email', ''))
    for nume, info in date['clienti'].items()
}
produse = {nume: Produs(nume, pret) for nume, pret in date['produse'].items()}

# Add initial data if not present in the file
if not clienti:
    clienti = {
        'Client1': Client('Client1', 1000, 1000, '123456789', 'ID001', 'client1@example.com'),
        'Client2': Client('Client2', 1500, 1500, '987654321', 'ID002', 'client2@example.com')
    }
    date['clienti'] = {
        nume: {
            'credit': client.credit,
            'credit_initial': client.credit_initial,
            'numar_telefon': client.numar_telefon,
            'id_unic': client.id_unic,
            'email': client.email
        }
        for nume, client in clienti.items()
    }
    salveaza_date(date)

if not produse:
    produse = {
        'Produs1': Produs('Produs1', 200),
        'Produs2': Produs('Produs2', 300),
        'Produs3': Produs('Produs3', 400)
    }
    date['produse'] = {nume: produs.pret for nume, produs in produse.items()}
    salveaza_date(date)

# Navigation menu
with st.sidebar:
    selectat = st.radio("Navigare", ["Formular de Comandă", "Editare Clienți și Produse", "Raport Comenzi"])

# Order Form page
if selectat == "Formular de Comandă":
    st.title("Formular de Comandă")

    # Select client
    nume_client = st.selectbox("Selectați Clientul:", list(clienti.keys()))
    client = clienti[nume_client]

    # Select products and quantities (two columns)
    st.subheader("Selectați Produsele și Cantitățile:")
    col1, col2 = st.columns(2)
    cantitati = {}
    for nume_produs, produs in produse.items():
        with col1:
            cantitati[nume_produs] = st.number_input(f"{nume_produs} ({produs.pret} RON pe unitate)", min_value=0, value=0)

    # Create order button
    if st.button("Creează Comandă"):
        produse_selectate = {nume: qty for nume, qty in cantitati.items() if qty > 0}
        pret_total = sum(produse[nume].pret * qty for nume, qty in produse_selectate.items())

        if pret_total > client.credit:
            st.error(f"Credit insuficient. Credit disponibil: {client.credit} RON")
        else:
            client.credit -= pret_total
            st.success(f"Comandă creată! Credit rămas: {client.credit} RON")

            # Update client data and save to JSON file
            date['clienti'][nume_client]['credit'] = client.credit
            salveaza_date(date)

            # Store order details in data
            date['comenzi'].setdefault(nume_client, [])
            date['comenzi'][nume_client].append({
                'data': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'produse': produse_selectate,
                'pret_total': pret_total
            })
            salveaza_date(date)

            # Display order details
            st.subheader("Detalii Comandă:")
            for nume, qty in produse_selectate.items():
                st.write(f"{nume}: {qty} unități - {produse[nume].pret * qty} RON total")
            st.write(f"Pret total: {pret_total} RON")

    # Display current client credit
    st.subheader("Credit Curent")
    st.write(f"Client: {client.nume}")
    st.write(f"Credit disponibil: {client.credit} RON")

# Edit Clients and Products page
elif selectat == "Editare Clienți și Produse":
    st.title("Editare Clienți și Produse")

    # Edit Clients
    st.subheader("Editare Clienți")
    nume_client = st.selectbox("Selectați Clientul pentru Editare:", list(clienti.keys()))
    nume_client_nou = st.text_input(f"Nume Client Nou pentru {nume_client}:", value=nume_client)
    credit_initial_client_nou = st.number_input(f"Credit Initial pentru {nume_client} (RON):", value=clienti[nume_client].credit_initial)
    numar_telefon_client_nou = st.text_input(f"Număr Telefon pentru {nume_client}:", value=clienti[nume_client].numar_telefon)
    id_unic_client_nou = st.text_input(f"ID Unic pentru {nume_client}:", value=clienti[nume_client].id_unic)
    email_client_nou = st.text_input(f"Adresă Email pentru {nume_client}:", value=clienti[nume_client].email)

    # Reset credit button for selected client
    if st.button("Resetare Credit"):
        clienti[nume_client].credit = clienti[nume_client].credit_initial
        date['clienti'][nume_client]['credit'] = clienti[nume_client].credit
        salveaza_date(date)
        st.success(f"Credit pentru {nume_client} a fost resetat la {clienti[nume_client].credit_initial} RON.")

    elif st.button("Actualizare Client"):
        if nume_client in clienti:
            del clienti[nume_client]
        clienti[nume_client_nou] = Client(nume_client_nou, credit_initial_client_nou, credit_initial_client_nou, numar_telefon_client_nou, id_unic_client_nou, email_client_nou)
        date['clienti'][nume_client_nou] = {
            'credit': credit_initial_client_nou,
            'credit_initial': credit_initial_client_nou,
            'numar_telefon': numar_telefon_client_nou,
            'id_unic': id_unic_client_nou,
            'email': email_client_nou
        }
        if nume_client != nume_client_nou:
            del date['clienti'][nume_client]
            if nume_client in date['comenzi']:
                date['comenzi'][nume_client_nou] = date['comenzi'][nume_client]
                del date['comenzi'][nume_client]
        salveaza_date(date)
