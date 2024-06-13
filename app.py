import streamlit as st
import json

# Funcție pentru citirea bazei de date din fișierul JSON
def citeste_baza_date():
    try:
        with open('data.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Funcție pentru salvarea bazei de date în fișierul JSON
def salveaza_baza_date(data):
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)

# Funcție pentru afișarea paginii principale
def afiseaza_pagina_principala():
    st.title('Gestionare Client și Produse')

    data = citeste_baza_date()

    # Selectare client existent și adăugare produse
    st.header('Selectare Client și Adăugare Produse')
    client_selectat = st.selectbox('Selectați clientul:', list(data.keys()))

    if client_selectat:
        client = data[client_selectat]
        credit_initial = client.get('credit_initial', 0)
        st.write(f"Credit disponibil pentru {client_selectat}: {credit_initial} RON")

        # Adăugare produse
        st.subheader('Adăugare Produse')
        produs = st.text_input('Numele produsului:')
        pret = st.number_input('Pretul produsului:', min_value=0.0, step=0.01)

        if st.button('Adaugă produs'):
            if 'produse' not in client:
                client['produse'] = []

            client['produse'].append({'nume': produs, 'pret': pret})
            credit_initial -= pret
            client['credit_initial'] = credit_initial
            salveaza_baza_date(data)
            st.success('Produs adăugat cu succes!')

    # Notificare dacă creditul este insuficient
    if credit_initial <= 0:
        st.warning('Creditul este insuficient!')

# Funcție pentru afișarea paginii de adăugare client nou
def afiseaza_pagina_adauga_client_nou():
    st.title('Adăugare Client Nou')

    # Formular pentru adăugarea unui client nou
    id_unic = st.text_input('ID Unic:')
    nume = st.text_input('Nume:')
    prenume = st.text_input('Prenume:')
    telefon = st.text_input('Telefon:')
    email = st.text_input('Email:')

    if st.button('Adaugă Client Nou'):
        data = citeste_baza_date()
        if id_unic in data:
            st.error('Clientul cu acest ID unic există deja!')
        else:
            data[id_unic] = {
                'nume': nume,
                'prenume': prenume,
                'telefon': telefon,
                'email': email,
                'credit_initial': 0,  # Inițializare credit
                'produse': []  # Lista produselor achiziționate
            }
            salveaza_baza_date(data)
            st.success('Clientul a fost adăugat cu succes!')

# Funcție pentru afișarea paginii de gestionare a produselor
def afiseaza_pagina_gestioneaza_produse():
    st.title('Gestionare Produse')

    data = citeste_baza_date()

    # Listare produse existente și editare preț
    st.header('Editare Produse')
    for client_id, client_data in data.items():
        st.subheader(f"Produse pentru {client_data['nume']} {client_data['prenume']}")
        if 'produse' in client_data:
            for produs in client_data['produse']:
                st.write(f"Nume: {produs['nume']}, Pret: {produs['pret']}")

                # Formular pentru editarea prețului produsului
                nou_pret = st.number_input('Noul pret:', min_value=0.0, step=0.01, value=produs['pret'])

                if st.button('Salvează modificări'):
                    produs['pret'] = nou_pret
                    salveaza_baza_date(data)
                    st.success('Prețul produsului a fost actualizat cu succes!')

# Funcție pentru afișarea paginii de raport complet al vânzărilor
def afiseaza_pagina_raport_complet():
    st.title('Raport Complet al Vânzărilor')

    data = citeste_baza_date()

    # Listare vânzări pentru fiecare client
    for client_id, client_data in data.items():
        st.subheader(f"Raport pentru {client_data['nume']} {client_data['prenume']}")
        if 'produse' in client_data:
            total_vanzari = sum(produs['pret'] for produs in client_data['produse'])
            st.write(f"Total vânzări: {total_vanzari} RON")


# Funcție principală pentru rutarea paginilor în funcție de selecția utilizatorului
def main():
    st.sidebar.title('Meniu')
    optiune = st.sidebar.selectbox('Selectați o opțiune:',
                                    ['Pagina Principală', 'Adăugare Client Nou', 'Gestionare Produse', 'Raport Complet Vânzări'])

    if optiune == 'Pagina Principală':
        afiseaza_pagina_principala()
    elif optiune == 'Adăugare Client Nou':
        afiseaza_pagina_adauga_client_nou()
    elif optiune == 'Gestionare Produse':
        afiseaza_pagina_gestioneaza_produse()
    elif optiune == 'Raport Complet Vânzări':
        afiseaza_pagina_raport_complet()

if __name__ == '__main__':
    main()
