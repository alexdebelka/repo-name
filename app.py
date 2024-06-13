import streamlit as st
import json
import os
from datetime import datetime

# Definirea claselor Client și Product
class Client:
    def __init__(self, name, credit, initial_credit):
        self.name = name
        self.credit = credit
        self.initial_credit = initial_credit

class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

# Fișierul pentru stocarea datelor
DATA_FILE = 'data.json'

# Funcții pentru a citi și scrie datele în fișierul JSON
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
            return data
    else:
        return {'clients': {}, 'products': {}}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

# Încărcarea datelor existente
data = load_data()

# Crearea dicționarelor pentru clienți și produse din datele încărcate
clients = {name: Client(name, info['credit'], info.get('initial_credit', info['credit'])) for name, info in data['clients'].items()}
products = {name: Product(name, price) for name, price in data['products'].items()}

# Adăugarea unor date inițiale dacă nu există în fișier
if not clients:
    clients = {
        'Client1': Client('Client1', 1000, 1000),
        'Client2': Client('Client2', 1500, 1500)
    }
    data['clients'] = {name: {'credit': client.credit, 'initial_credit': client.initial_credit} for name, client in clients.items()}
    save_data(data)

if not products:
    products = {
        'Produs1': Product('Produs1', 200),
        'Produs2': Product('Produs2', 300),
        'Produs3': Product('Produs3', 400)
    }
    data['products'] = {name: product.price for name, product in products.items()}
    save_data(data)

# Meniul de navigare
with st.sidebar:
    selected = st.radio("Navigare", ["Formular Comandă", "Editare Clienți și Produse", "Raport Comenzi"])

# Pagina de Formular Comandă
if selected == "Formular Comandă":
    st.title("Formular Comandă")

    # Selectarea clientului
    client_name = st.selectbox("Selectează Clientul:", list(clients.keys()))
    client = clients[client_name]

    # Selectarea produselor și cantităților
    st.subheader("Selectează Produsele și Cantitățile:")
    quantities = {}
    for product_name, product in products.items():
        quantities[product_name] = st.number_input(f"{product_name} ({product.price} RON per unitate)", min_value=0, value=0)

    # Buton pentru creare comandă
    if st.button("Creează Comandă"):
        selected_products = {name: qty for name, qty in quantities.items() if qty > 0}
        total_price = sum(products[name].price * qty for name, qty in selected_products.items())

        if total_price > client.credit:
            st.error(f"Credit insuficient. Credit disponibil: {client.credit} RON")
        else:
            client.credit -= total_price
            st.success(f"Comandă creată! Credit rămas: {client.credit} RON")

            # Actualizarea datelor clientului și salvarea în fișierul JSON
            data['clients'][client_name]['credit'] = client.credit
            save_data(data)

            # Afișarea detaliilor comenzii
            st.subheader("Detalii Comandă:")
            for name, qty in selected_products.items():
                st.write(f"{name}: {qty} unități - {products[name].price * qty} RON total")
            st.write(f"Preț total: {total_price} RON")

    # Afișarea creditului curent al clientului
    st.subheader("Credit Curent")
    st.write(f"Client: {client.name}")
    st.write(f"Credit disponibil: {client.credit} RON")

# Pagina de Editare Clienți și Produse
elif selected == "Editare Clienți și Produse":
    st.title("Editare Clienți și Produse")

    # Editare Clienți
    st.subheader("Editare Clienți")
    client_name = st.selectbox("Selectează Clientul pentru Editare:", list(clients.keys()))
    new_client_name = st.text_input("Nume Client Nou:", client_name)
    new_client_credit = st.number_input("Credit Inițial (RON):", value=clients[client_name].initial_credit)

    # Buton pentru resetarea creditului pentru clientul selectat
    if st.button("Resetează Creditul"):
        clients[client_name].credit = clients[client_name].initial_credit
        data['clients'][client_name]['credit'] = clients[client_name].credit
        save_data(data)
        st.success(f"Creditul pentru {client_name} a fost resetat la {clients[client_name].initial_credit} RON.")

    if st.button("Actualizează Client"):
        if client_name in clients:
            del clients[client_name]
        clients[new_client_name] = Client(new_client_name, new_client_credit, new_client_credit)
        data['clients'][new_client_name] = {'credit': new_client_credit, 'initial_credit': new_client_credit}
        if client_name != new_client_name:
            del data['clients'][client_name]
        save_data(data)
        st.success(f"Clientul {client_name} a fost actualizat la {new_client_name} cu un credit de {new_client_credit} RON.")

    # Adăugare Client Nou
    st.subheader("Adăugare Client Nou")
    new_client_name = st.text_input("Nume Client Nou:")
    new_client_credit = st.number_input("Credit Inițial (RON):", value=0)

    if st.button("Adaugă Client Nou"):
        if new_client_name.strip() == "":
            st.warning("Numele clientului nu poate fi gol!")
        elif new_client_name in clients:
            st.warning(f"Clientul {new_client_name} există deja!")
        else:
            clients[new_client_name] = Client(new_client_name, new_client_credit, new_client_credit)
            data['clients'][new_client_name] = {'credit': new_client_credit, 'initial_credit': new_client_credit}
            save_data(data)
            st.success(f"Clientul {new_client_name} a fost adăugat cu succes!")

    # Editare Produse
    st.subheader("Editare Produse")
    product_name = st.selectbox("Selectează Produsul pentru Editare:", list(products.keys()))
    new_product_name = st.text_input("Nume Produs Nou:", product_name)
    new_product_price = st.number_input("Preț Produs Nou (RON):", value=products[product_name].price)

    if st.button("Actualizează Produs"):
        if product_name in products:
            del products[product_name]
        products[new_product_name] = Product(new_product_name, new_product_price)
        data['products'][new_product_name] = new_product_price
        if product_name != new_product_name:
            del data['products'][product_name]
        save_data(data)
        st.success(f"Produsul {product_name} a fost actualizat la {new_product_name} cu un preț de {new_product_price} RON.")

    # Adăugare Produs Nou
    st.subheader("Adăugare Produs Nou")
    new_product_name = st.text_input("Nume Produs Nou:")
    new_product_price = st.number_input("Preț Produs Nou (RON):", value=0)

    if st.button("Adaugă Produs Nou"):
        if new_product_name.strip() == "":
            st.warning("Numele produsului nu poate fi gol!")
        elif new_product_name in products:
            st.warning(f"Produsul {new_product_name} există deja!")
        else:
            products[new_product_name] = Product(new_product_name, new_product_price)
            data['products'][new_product_name] = new_product_price
            save_data(data)
            st.success(f"Produsul {new_product_name} a fost adăugat cu succes!")

# Pagina de Raport Comenzi
elif selected == "Raport Comenzi":
    st.title("Raport Comenzi")

    # Selectarea clientului pentru vizualizarea raportului
    client_name = st.selectbox("Selectează Clientul pentru Raport:", list(clients.keys()))
    client = clients[client
