import json
import streamlit as st
import os

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
    with open(file, 'w') as f:
        json.dump(data, f, indent=4)

# Funcție pentru adăugarea unui client nou
def add_client(name, email, phone):
    clients = read_json(CLIENTS_FILE)
    new_client = {
        'id': len(clients) + 1,
        'name': name,
        'email': email,
        'phone': phone,
        'credits': 0
    }
    clients.append(new_client)
    write_json(CLIENTS_FILE, clients)

# Funcție pentru găsirea unui client
def find_client(name):
    clients = read_json(CLIENTS_FILE)
    return [client for client in clients if client['name'] == name]

# Funcție pentru actualizarea creditelor unui client
def update_credits(client_id, amount):
    clients = read_json(CLIENTS_FILE)
    for client in clients:
        if client['id'] == client_id:
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

menu = ["Add Client", "Find Client", "Manage Products", "Update Credits"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Add Client":
    st.subheader("Add Client")
    name = st.text_input("Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone")
    if st.button("Add"):
        add_client(name, email, phone)
        st.success("Client added successfully")

elif choice == "Find Client":
    st.subheader("Find Client")
    name = st.text_input("Search by Name")
    if st.button("Search"):
        clients = find_client(name)
        if clients:
            st.write("Client Found: ", clients)
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
    for product in products:
        st.write(f"Name: {product['name']}, Price: {product['price']}")

elif choice == "Update Credits":
    st.subheader("Update Credits")
    client_id = st.number_input("Client ID", min_value=1)
    amount = st.number_input("Amount", min_value=-100.0, max_value=100.0)
    if st.button("Update"):
        update_credits(client_id, amount)
        st.success("Credits updated successfully")

# Eliminăm apelul st.run()
