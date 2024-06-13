import streamlit as st
import pandas as pd
import json

# Funcție pentru a încărca datele din fișierul JSON
def load_data(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

# Funcție pentru a salva datele înapoi în fișierul JSON
def save_data(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

# Funcție pentru afișarea paginii de adăugare/modificare produse
def add_modify_products(products):
    st.header("Adăugare/Modificare Produse")
    # Interfață pentru adăugare/modificare produse
    # Poți utiliza formulare pentru a adăuga și modifica produsele din lista `products`

# Funcție pentru afișarea paginii de rapoarte
def show_reports(transactions):
    st.header("Rapoarte")
    # Interfață pentru afișarea rapoartelor detaliate pe tranzacții

# Funcție pentru afișarea paginii de comenzi
def show_orders(clients, products):
    st.header("Formular Comenzi")
    # Interfață pentru a selecta clienți și produse și a plasa comenzi

    client_names = [client['name'] for client in clients]
    selected_client = st.selectbox("Selectați clientul:", client_names)

    product_names = [product['name'] for product in products]
    selected_products = st.multiselect("Selectați produsele:", product_names)

    if st.button("Plasează comanda"):
        # Poți implementa aici logica de plasare a comenzii și actualizarea tranzacțiilor în baza de date
        pass

# Funcția principală pentru aplicația Streamlit
def main():
    st.title("Aplicație de Comenzi")

    # Încărcare datelor din fișierul JSON
    data = load_data('data.json')

    # Extragere datelor
    clients = data.get('clients', [])
    products = data.get('products', [])
    transactions = data.get('transactions', [])

    # Pagina pentru adăugare/modificare produse
    add_modify_products(products)

    # Pagina pentru rapoarte
    show_reports(transactions)

    # Pagina pentru formularul de comenzi
    show_orders(clients, products)

    # Salvare date actualizate înapoi în fișierul JSON
    save_data(data, 'data.json')

if __name__ == "__main__":
    main()
