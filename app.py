import json
import streamlit as st
import os
import pandas as pd

# Fișierele JSON pentru stocarea datelor
CLIENTS_FILE = 'clients.json'
PRODUCTS_FILE = 'products.json'

# Funcții pentru gestionarea fișierelor JSON
def read_json(file):
    if not os.path.exists(file):
        with open(file, 'w') as f:
            json.dump([], f)
    with open(file, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def write_json(file, data):
    try:
        with open(file, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Succesfully written to {file}")
    except Exception as e:
        print(f"Error writing to {file}: {e}")

# Funcție pentru adăugarea unui client nou
def add_client(code, name, email, phone, credits):
    clients = read_json(CLIENTS_FILE)
    new_client = {
        'id': len(clients) + 1,
        'code': code.lower(),
        'name': name,
        'email': email,
        'phone': phone,
        'credits': credits
    }
    clients.append(new_client)
    write_json(CLIENTS_FILE, clients)

# Funcție pentru găsirea unui client după cod (case insensitive)
def find_client_by_code(code):
    clients = read_json(CLIENTS_FILE)
    return [client for client in clients if client['code'] == code.lower()]

# Funcție pentru actualizarea creditelor unui client
def update_credits(client_code, amount):
    clients = read_json(CLIENTS_FILE)
    for client in clients:
        if client['code'] == client_code.lower():
            client['credits'] += amount
    write_json(CLIENTS_FILE, clients)

# Funcție pentru adăugarea unui produs
def add_product(name, price):
    products = read_json(PRODUCTS_FILE)
    new_product = {
        'id': len(products) + 1,
        'name': name,
        'price': price
    }
    products.append(new_product)
    write_json(PRODUCTS_FILE, products)

# Funcție pentru listarea produselor
def get_products():
    return read_json(PRODUCTS_FILE)

# Interfața Streamlit
st.title("Cafenea Prepaid Card System")

menu = ["Add Client", "Find Client", "Manage Products", "Update Credits", "Purchase Products"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Add Client":
    st.subheader("Add Client")
    code = st.text_input("Code")
    name = st.text_input("Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone")
    credits = st.number_input("Credits (RON)", min_value=0.0)
    if st.button("Add"):
        add_client(code, name, email, phone, credits)
        st.success("Client added successfully")

elif choice == "Find Client":
    st.subheader("Find Client")
    code = st.text_input("Search by Code")
    if st.button("Search"):
        clients = find_client_by_code(code)
        if clients:
            df = pd.DataFrame(clients)
            df.rename(columns={'credits': 'credits (RON)'}, inplace=True)
            st.write("Client Found:")
            st.dataframe(df)
        else:
            st.warning("Client not found")

elif choice == "Manage Products":
    st.subheader("Manage Products")
    product_name = st.text_input("Product Name")
    product_price = st.number_input("Product Price", min_value=0.0)
    if st.button("Add Product"):
        add_product(product_name, product_price)
        st.success("Product added successfully")
    st.subheader("Product List")
    products = get_products()
    df = pd.DataFrame(products)
    st.dataframe(df)

elif choice == "Update Credits":
    st.subheader("Update Credits")
    client_code = st.text_input("Client Code")
    amount = st.number_input("Amount (RON)", min_value=-100.0, max_value=100.0)
    if st.button("Update"):
        update_credits(client_code, amount)
        st.success("Credits updated successfully")

elif choice == "Purchase Products":
    st.subheader("Purchase Products")
    client_code = st.text_input("Client Code")
    products = get_products()
    product_names = [product['name'] for product in products]
    selected_products = st.multiselect("Select Products", product_names)
    if st.button("Purchase"):
        clients = find_client_by_code(client_code)
        if not clients:
            st.warning("Client not found")
        else:
            client = clients[0]
            total_cost = sum(product['price'] for product in products if product['name'] in selected_products)
            if client['credits'] >= total_cost:
                client['credits'] -= total_cost
                write_json(CLIENTS_FILE, clients)
                st.success(f"Purchase successful! Total cost: {total_cost} RON. Remaining credits: {client['credits']} RON.")
            else:
                st.error(f"Not enough credits. Total cost: {total_cost} RON. Available credits: {client['credits']} RON.")

# Eliminăm apelul st.run()
