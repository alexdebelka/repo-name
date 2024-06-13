from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

# Încărcăm datele din fișierul JSON
with open('data.json', 'r') as f:
    data = json.load(f)

clients = data['clients']
products = data['products']

# Pagina principală care afișează formularul de comandă
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        client_id = int(request.form['client'])
        selected_client = next(client for client in clients if client['id'] == client_id)
        
        selected_products = []
        for product in products:
            product_id_str = 'product_{}'.format(product['id'])
            if product_id_str in request.form:
                quantity = int(request.form[product_id_str])
                if quantity > 0:
                    selected_products.append({
                        'id': product['id'],
                        'name': product['name'],
                        'quantity': quantity,
                        'total_price': quantity * product['price']
                    })
        
        # Aici poți face ce vrei cu datele, de exemplu, le poți salva într-o bază de date sau poți să le afișezi pe o altă pagină
        return render_template('order_summary.html', client=selected_client, products=selected_products)
    
    return render_template('order_form.html', clients=clients, products=products)

if __name__ == '__main__':
    app.run(debug=True)
