import json
import streamlit as st
import os
import pandas as pd
from datetime import datetime

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
        print(f"Successfully written to {file}")
    except Exception as e:
        print(f"Error writing to {file}: {e}")

# Funcție pentru adăugarea unui client nou
def add_client(code, name, email, phone, credits):
    clients = read_json(CLIENTS_FILE)
    new_client = {
        'id': len(clients) + 1,
        'code': code.lower(),
        'name': name.lower(),
        'email': email,
        'phone': phone,
        'credits': credits,
        'history': []
    }
    clients.append(new_client)
    write_json(CLIENTS_FILE, clients)

# Funcție pentru găsirea unui client după cod (case insensitive)
def find_client_by_code(code):
    clients = read_json(CLIENTS_FILE)
    return [client for client in clients if client['code'] == code.lower()]

# Funcție pentru găsirea unui client după nume (case insensitive)
def find_client_by_name(name):
    clients = read_json(CLIENTS_FILE)
    return [client for client in clients if client['name'] == name.lower()]

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

# Funcție pentru adăugarea achiziției în istoricul clientului
def add_purchase_history(client, products_purchased):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for product_name, quantity in products_purchased.items():
        if quantity > 0:
            client['history'].append({
                'timestamp': timestamp,
                'product': product_name,
                'quantity': quantity,
                'total_cost': quantity * next(product['price'] for product in get_products() if product['name'] == product_name)
            })

# Interfața Streamlit
st.title("Cafenea Prepaid Card System")

menu = ["Add Client", "Find Client", "Manage Products", "Update Credits", "Purchase Products", "View History"]
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
    search_by = st.radio("Search by", ("Code", "Name"))
    if search_by == "Code":
        code = st.text_input("Enter Code")
        if st.button("Search by Code"):
            clients = find_client_by_code(code)
            if clients:
                df = pd.DataFrame(clients)
                df.rename(columns={'credits': 'credits (RON)'}, inplace=True)
                st.write("Client Found:")
                st.dataframe(df)
            else:
                st.warning("Client not found")
    elif search_by == "Name":
        name = st.text_input("Enter Name")
        if st.button("Search by Name"):
            clients = find_client_by_name(name)
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
    search_by = st.radio("Search Client by", ("Code", "Name"))
    if search_by == "Code":
        client_code = st.text_input("Enter Client Code")
        client_name = None
    elif search_by == "Name":
        client_name = st.text_input("Enter Client Name")
        client_code = None

    products = get_products()
    product_quantities = {product['name']: st.number_input(f"{product['name']} Quantity", min_value=0, step=1) for product in products}

    if st.button("Purchase"):
        if search_by == "Code":
            clients = find_client_by_code(client_code)
        elif search_by == "Name":
            clients = find_client_by_name(client_name)
        
        if not clients:
            st.warning("Client not found")
        else:
            client = clients[0]
            total_cost = sum(product['price'] * quantity for product in products for name, quantity in product_quantities.items() if product['name'] == name)
            if client['credits'] >= total_cost:
                client['credits'] -= total_cost
                # Adăugăm achiziția în istoricul clientului
                add_purchase_history(client, product_quantities)
                write_json(CLIENTS_FILE, clients)
                st.success(f"Purchase successful! Total cost: {total_cost} RON. Remaining credits: {client['credits']} RON.")
            else:
                st.error(f"Not enough credits. Total cost: {total_cost} RON. Available credits: {client['credits']} RON.")

elif choice == "View History":
    st.subheader("View Purchase History")
    client_code = st.text_input("Enter Client Code")
    if st.button("View History"):
        clients = find_client_by_code(client_code)
        if clients:
            client = clients[0]
            if 'history' in client and client['history']:
                history_df = pd.DataFrame(client['history'])
                st.write(f"Purchase History for {client['name'].capitalize()}:")
                st.dataframe(history_df)
            else:
                st.write(f"No purchase history for {client['name'].capitalize()}.")
        else:
            st.warning("Client not found")
