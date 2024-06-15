import json
import streamlit as st
import os
import pandas as pd
from datetime import datetime

# CSS pentru a schimba culorile și stilurile
st.markdown("""
    <style>
    .stButton>button {
        background-color: #FAD02C;
        color: black;
    }
    .stRadio>div>div>label {
        color: #FAD02C;
    }
    .stSidebar>div {
        background-color: #FAD02C;
    }
    .stTextInput>div>div>input {
        color: black;
    }
    .stNumberInput>div>div>input {
        color: black;
    }
    .stDataFrame>div>div>div>table {
        background-color: #FAD02C;
    }
    .css-1aumxhk, .css-1aumxhk a {
        color: #FAD02C;
    }
    .css-1aumxhk .css-1aumxhk, .css-1aumxhk .css-1aumxhk a {
        font-size: 1.2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Fișierele JSON pentru stocarea datelor
CLIENTS_FILE = 'clients.json'
PRODUCTS_FILE = 'products.json'

# Date default
default_clients = [
    {
        'id': 1,
        'code': '10',
        'name': 'edu',
        'email': 'edu@edu.ro',
        'phone': '1234567890',
        'credits': 100.0,
        'history': []
    }
]

default_products = [
    {'id': 1, 'name': 'Espresso', 'price': 8.0},
    {'id': 2, 'name': 'Mocha', 'price': 14.0},
    {'id': 3, 'name': 'Latte', 'price': 10.0},
    {'id': 4, 'name': 'Cappuccino', 'price': 12.0},
    {'id': 5, 'name': 'Americano', 'price': 9.0},
    {'id': 6, 'name': 'Macchiato', 'price': 10.0},
    {'id': 7, 'name': 'Flat White', 'price': 11.0},
    {'id': 8, 'name': 'Affogato', 'price': 13.0},
    {'id': 9, 'name': 'Black Coffee', 'price': 7.0},
    {'id': 10, 'name': 'Irish Coffee', 'price': 15.0},
    {'id': 11, 'name': 'Iced Coffee', 'price': 10.0},
    {'id': 12, 'name': 'Cold Brew', 'price': 14.0},
    {'id': 13, 'name': 'Nitro Coffee', 'price': 16.0},
    {'id': 14, 'name': 'Turkish Coffee', 'price': 8.0},
    {'id': 15, 'name': 'Frappe', 'price': 12.0},
    {'id': 16, 'name': 'Cortado', 'price': 11.0}
]

# Funcții pentru gestionarea fișierelor JSON
def read_json(file, default_data):
    if not os.path.exists(file):
        with open(file, 'w') as f:
            json.dump(default_data, f)
    with open(file, 'r') as f:
        try:
            data = json.load(f)
            if not data:
                data = default_data
                write_json(file, data)
            return data
        except json.JSONDecodeError:
            return default_data

def write_json(file, data):
    try:
        with open(file, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        st.error(f"Error writing to {file}: {e}")

# Funcție pentru adăugarea unui client nou
def add_client(code, name, email, phone, credits):
    clients = read_json(CLIENTS_FILE, default_clients)
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

# Funcție pentru găsirea unui client după cod
def find_client_by_code(code):
    clients = read_json(CLIENTS_FILE, default_clients)
    return [client for client in clients if client['code'] == code.lower()]

# Funcție pentru găsirea unui client după nume
def find_client_by_name(name):
    clients = read_json(CLIENTS_FILE, default_clients)
    return [client for client in clients if client['name'] == name.lower()]

# Funcție pentru actualizarea creditelor unui client
def update_credits(client_code, amount):
    clients = read_json(CLIENTS_FILE, default_clients)
    for client in clients:
        if client['code'] == client_code.lower():
            client['credits'] += amount
    write_json(CLIENTS_FILE, clients)

# Funcție pentru adăugarea unui produs
def add_product(name, price):
    products = read_json(PRODUCTS_FILE, default_products)
    new_product = {
        'id': len(products) + 1,
        'name': name,
        'price': price
    }
    products.append(new_product)
    write_json(PRODUCTS_FILE, products)

# Funcție pentru actualizarea unui produs
def update_product(product_id, name, price):
    products = read_json(PRODUCTS_FILE, default_products)
    for product in products:
        if product['id'] == product_id:
            product['name'] = name
            product['price'] = price
    write_json(PRODUCTS_FILE, products)

# Funcție pentru listarea produselor
def get_products():
    return read_json(PRODUCTS_FILE, default_products)

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
st.title("CAFIZZIO")

menu = ["Purchase Products", "Find Client", "View History", "Add Client", "Update Credits", "Manage Products"]
choice = st.sidebar.radio("Menu", menu)

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
    products = get_products()
    product_names = [product['name'] for product in products]
    selected_product_name = st.selectbox("Select Product to Edit", product_names)
    selected_product = next((product for product in products if product['name'] == selected_product_name), None)
    
    if selected_product:
        new_name = st.text_input("Product Name", value=selected_product['name'])
        new_price = st.number_input("Product Price", min_value=0.0, value=selected_product['price'])
        if st.button("Update Product"):
            update_product(selected_product['id'], new_name, new_price)
            st.success("Product updated successfully")

    st.subheader("Add New Product")
    product_name = st.text_input("New Product Name")
    product_price = st.number_input("New Product Price", min_value=0.0)
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
        if st.button("Check Client", key="check_client_code"):
            clients = find_client_by_code(client_code)
            if clients:
                st.success("Client found")
                st.session_state['client'] = clients[0]
            else:
                st.error("Client not found")
    elif search_by == "Name":
        client_name = st.text_input("Enter Client Name")
        if st.button("Check Client", key="check_client_name"):
            clients = find_client_by_name(client_name)
            if clients:
                st.success("Client found")
                st.session_state['client'] = clients[0]
            else:
                st.error("Client not found")

    client = st.session_state.get('client', None)
    
    if client:
        products = get_products()
        cols = st.columns(8)
        product_quantities = {}
        for i, product in enumerate(products):
            with cols[i % 8]:
                product_quantities[product['name']] = st.number_input(f"{product['name']} Quantity", min_value=0, step=1)
        
        if st.button("Purchase"):
            total_cost = sum(product['price'] * quantity for product in products for name, quantity in product_quantities.items() if product['name'] == name)
            if client['credits'] >= total_cost:
                client['credits'] -= total_cost
                add_purchase_history(client, product_quantities)
                clients = read_json(CLIENTS_FILE, default_clients)
                for c in clients:
                    if c['id'] == client['id']:
                        c.update(client)
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

