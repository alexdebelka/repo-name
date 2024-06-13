import streamlit as st
import json
import os
from datetime import datetime

# Define Client and Product classes
class Client:
    def __init__(self, name, credit, initial_credit, phone_number, unique_id, email):
        self.name = name
        self.credit = credit
        self.initial_credit = initial_credit
        self.phone_number = phone_number
        self.unique_id = unique_id
        self.email = email

class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

# File to store data
DATA_FILE = 'data.json'

# Functions to read and write data to JSON file
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

# Loading existing data
data = load_data()

# Creating dictionaries for clients and products from loaded data
clients = {
    name: Client(name, info['credit'], info.get('initial_credit', info['credit']), info.get('phone_number', ''), info.get('unique_id', ''), info.get('email', ''))
    for name, info in data['clients'].items()
}
products = {name: Product(name, price) for name, price in data['products'].items()}

# Adding initial data if not present in the file
if not clients:
    clients = {
        'Client1': Client('Client1', 1000, 1000, '123456789', 'ID001', 'client1@example.com'),
        'Client2': Client('Client2', 1500, 1500, '987654321', 'ID002', 'client2@example.com')
    }
    data['clients'] = {
        name: {
            'credit': client.credit,
            'initial_credit': client.initial_credit,
            'phone_number': client.phone_number,
            'unique_id': client.unique_id,
            'email': client.email
        }
        for name, client in clients.items()
    }
    save_data(data)

if not products:
    products = {
        'Produs1': Product('Produs1', 200),
        'Produs2': Product('Produs2', 300),
        'Produs3': Product('Produs3', 400)
    }
    data['products'] = {name: product.price for name, product in products.items()}
    save_data(data)

# Navigation menu
with st.sidebar:
    selected = st.radio("Navigation", ["Order Form", "Edit Clients and Products", "Order Report"])

# Order Form Page
if selected == "Order Form":
    st.title("Order Form")

    # Selecting the client
    client_name = st.selectbox("Select Client:", list(clients.keys()))
    client = clients[client_name]

    # Selecting products and quantities (two columns)
    st.subheader("Select Products and Quantities:")
    col1, col2 = st.columns(2)
    quantities = {}
    for product_name, product in products.items():
        with col1:
            quantities[product_name] = st.number_input(f"{product_name} ({product.price} RON per unit)", min_value=0, value=0)

    # Button to create order
    if st.button("Create Order"):
        selected_products = {name: qty for name, qty in quantities.items() if qty > 0}
        total_price = sum(products[name].price * qty for name, qty in selected_products.items())

        if total_price > client.credit:
            st.error(f"Insufficient credit. Available credit: {client.credit} RON")
        else:
            client.credit -= total_price
            st.success(f"Order created! Remaining credit: {client.credit} RON")

            # Updating client data and saving to JSON file
            data['clients'][client_name]['credit'] = client.credit
            save_data(data)

            # Storing order details in data
            if 'orders' not in data:
                data['orders'] = {}
            if client_name not in data['orders']:
                data['orders'][client_name] = []
            data['orders'][client_name].append({
                'datetime': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'products': selected_products,
                'total_price': total_price
            })
            save_data(data)

            # Displaying order details
            st.subheader("Order Details:")
            for name, qty in selected_products.items():
                st.write(f"{name}: {qty} units - {products[name].price * qty} RON total")
            st.write(f"Total price: {total_price} RON")

    # Displaying current credit of the client
    st.subheader("Current Credit")
    st.write(f"Client: {client.name}")
    st.write(f"Available credit: {client.credit} RON")

# Edit Clients and Products Page
elif selected == "Edit Clients and Products":
    st.title("Edit Clients and Products")

    # Edit Clients
    st.subheader("Edit Clients")
    client_name = st.selectbox("Select Client for Edit:", list(clients.keys()))
    new_client_name = st.text_input("New Client Name:", client_name)
    new_client_credit = st.number_input("Initial Credit (RON):", value=clients[client_name].initial_credit)
    new_client_phone_number = st.text_input("Phone Number:", value=clients[client_name].phone_number)
    new_client_unique_id = st.text_input("Unique ID:", value=clients[client_name].unique_id)
    new_client_email = st.text_input("Email Address:", value=clients[client_name].email)

    # Button to reset credit for selected client
    if st.button("Reset Credit"):
        clients[client_name].credit = clients[client_name].initial_credit
        data['clients'][client_name]['credit'] = clients[client_name].credit
        save_data(data)
        st.success(f"Credit for {client_name} has been reset to {clients[client_name].initial_credit} RON.")

    if st.button("Update Client"):
        if client_name in clients:
            del clients[client_name]
        clients[new_client_name] = Client(new_client_name, new_client_credit, new_client_credit, new_client_phone_number, new_client_unique_id, new_client_email)
        data['clients'][new_client_name] = {
            'credit': new_client_credit,
            'initial_credit': new_client_credit,
            'phone_number': new_client_phone_number,
            'unique_id': new_client_unique_id,
            'email': new_client_email
        }
        if client_name != new_client_name:
            del data['clients'][client_name]
        save_data(data)
        st.success(f"Client {client_name} has been updated to {new_client_name} with a credit of {new_client_credit} RON.")

    # Add New Client
    st.subheader("Add New Client")
    new_client_name = st.text_input("New Client Name:")
    new_client_credit = st.number_input("Initial Credit (RON):", value=0)
    new_client_phone_number = st.text_input("Phone Number:")
    new_client_unique_id = st.text_input("Unique ID:")
    new_client_email = st.text_input("Email Address:")

    if st.button("Add New Client"):
        if new_client_name.strip() == "":
            st.warning("Client name cannot be empty!")
        elif new_client_name in clients:
            st.warning(f"Client {new_client_name} already exists!")
        else:
            clients[new_client_name] = Client(new_client_name, new_client_credit, new_client_credit, new_client_phone_number, new_client_unique_id, new_client_email)
            data['clients'][new_client_name] = {
                'credit': new_client_credit,
                'initial_credit': new_client_credit,
                'phone_number': new_client_phone_number,
                'unique_id': new_client_unique_id,
                'email': new_client_email
            }
            save_data(data)
            st.success(f"Client {new_client_name} has been added successfully!")

    # Edit Products
    st.subheader("Edit Products")
    product_name = st.selectbox("Select Product for Edit:", list(products.keys()))
    new_product_name = st.text_input("New Product Name:", product_name)
    new_product_price = st.number_input("New Product Price (RON):", value=products[product_name].price)

    if st.button("Update Product"):
        if product_name in products:
            del products[product_name]
        products[new_product_name] = Product(new_product_name, new_product_price)
        data['products'][new_product_name] = new_product_price
        if product_name != new_product_name:
            del data['products'][product_name]
        save_data(data)
        st.success(f"Product {product_name} has been updated to {new_product_name} with a price of {new_product_price} RON.")

    # Add New Product
    st.subheader("Add New Product")
    new_product_name = st.text_input("New Product Name:")
    new_product_price = st.number_input("New Product Price (RON):", value=0)

    if st.button("Add New Product"):
        if new_product_name.strip() == "":
            st.warning("Product name cannot be empty!")
        elif new_product_name in products:
            st.warning(f"Product {new_product_name} already exists!")
        else:
            products[new_product_name] = Product
