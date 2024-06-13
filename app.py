import streamlit as st
import json
import os
from datetime import datetime

# Definirea claselor Client și Produs
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

# Fișier pentru stocarea datelor
FISIER_DATE = 'data.json'

# Funcții pentru citirea și scrierea datelor în fișierul JSON
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

# Încărcarea datelor existente
date = incarca_date()

# Verificăm și inițializăm dicționarele pentru clienți, produse și comenzi dacă nu există
if 'clienti' not in date:
    date['clienti'] = {}
if 'produse' not in date:
    date['produse'] = {}
if 'comenzi' not in date:
    date['comenzi'] = {}

# Crearea dicționarelor pentru clienți și produse din datele încărcate
clienti = {
    nume: Client(nume, info['credit'], info.get('credit_initial', info['credit']), info.get('numar_telefon', ''), info.get('id_unic', ''), info.get('email', ''))
    for nume, info in date['clienti'].items()
}
produse = {nume: Produs(nume, pret) for nume, pret in date['produse'].items()}

# Adăugarea datelor inițiale dacă nu sunt prezente în fișier
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

# Meniul de navigare
with st.sidebar:
    selectat = st.radio("Navigare", ["Formular de Comandă", "Editare Clienți și Produse", "Raport Comenzi"])

# Pagina Formular de Comandă
if selectat == "Formular de Comandă":
    st.title("Formular de Comandă")

    # Selectarea clientului
    nume_client = st.selectbox("Selectați Clientul:", list(clienti.keys()))
    client = clienti[nume_client]

    # Selectarea produselor și a cantităților (două coloane)
    st.subheader("Selectați Produsele și Cantitățile:")
    col1, col2 = st.columns(2)
    cantitati = {}
    for nume_produs, produs in produse.items():
        with col1:
            cantitati[nume_produs] = st.number_input(f"{nume_produs} ({produs.pret} RON pe unitate)", min_value=0, value=0)

    # Buton pentru crearea comenzii
    if st.button("Creează Comandă"):
        produse_selectate = {nume: qty for nume, qty in cantitati.items() if qty > 0}
        pret_total = sum(produse[nume].pret * qty for nume, qty in produse_selectate.items())

        if pret_total > client.credit:
            st.error(f"Credit insuficient. Credit disponibil: {client.credit} RON")
        else:
            client.credit -= pret_total
            st.success(f"Comandă creată! Credit rămas: {client.credit} RON")

            # Actualizare date client și salvare în fișierul JSON
            date['clienti'][nume_client]['credit'] = client.credit
            salveaza_date(date)

            # Stocare detalii comandă în date
            date['comenzi'].setdefault(nume_client, [])
            date['comenzi'][nume_client].append({
                'data': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'produse': produse_selectate,
                'pret_total': pret_total
            })
            salveaza_date(date)

            # Afișare detalii comandă
            st.subheader("Detalii Comandă:")
            for nume, qty in produse_selectate.items():
                st.write(f"{nume}: {qty} unități - {produse[nume].pret * qty} RON total")
            st.write(f"Pret total: {pret_total} RON")

    # Afișare credit curent al clientului
    st.subheader("Credit Curent")
    st.write(f"Client: {client.nume}")
    st.write(f"Credit disponibil: {client.credit} RON")

# Pagina Editare Clienți și Produse
elif selectat == "Editare Clienți și Produse":
    st.title("Editare Clienți și Produse")

    # Editare Clienți
    st.subheader("Editare Clienți")
    nume_client = st.selectbox("Selectați Clientul pentru Editare:", list(clienti.keys()))
    nume_client_nou = st.text_input(f"Nume Client Nou pentru {nume_client}:", value=nume_client)
    credit_initial_client_nou = st.number_input(f"Credit Initial pentru {nume_client} (RON):", value=clienti[nume_client].credit_initial)
    numar_telefon_client_nou = st.text_input(f"Număr Telefon pentru {nume_client}:", value=clienti[nume_client].numar_telefon)
    id_unic_client_nou = st.text_input(f"ID Unic pentru {nume_client}:", value=clienti[nume_client].id_unic)
    email_client_nou = st.text_input(f"Adresă Email pentru {nume_client}:", value=clienti[nume_client].email)

    # Buton pentru resetarea creditului pentru clientul selectat
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
            'credit_initial': credit_initial_client_n
