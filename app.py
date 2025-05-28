from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
app = Flask('_name_')
BASE_URL = "https://hashkeys.space/71/"


def scrape_addresses():
    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.content, 'html.parser')
    addresses = []
    rows = soup.select('tbody tr')
    for row in rows:
        columns = row.find_all('td')
        if len(columns) >= 2:
            key_hex = columns[0].text.strip()
            address = columns[1].text.strip()
            addresses.append((key_hex, address))
    return addresses


@app.route('/', methods=['GET', 'POST'])
def home():
    found_address = None
    if request.method == 'POST':
        address_to_check = request.form.get('address')
        addresses = scrape_addresses()
        for key_hex, address in addresses:
            if address == address_to_check:
                found_address = (key_hex, address)
                break
    return render_template('index.html', found_address=found_address)

    if '_name_' == '_main_':
        app.run(host='0.0.0.0', port=8000)  # Change port to 8080
