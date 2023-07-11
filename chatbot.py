from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/', methods=['POST'])
def index():
    data = request.get_json()
    source_currency = data['queryResult']['parameters']['unit-currency'][0]['currency']
    amount = data['queryResult']['parameters']['unit-currency'][0]['amount']
    target_currency = data['queryResult']['parameters']['currency-name'][0]
    print(source_currency)
    cf = fetch_conversion_factor(source_currency, target_currency)
    final_amount = amount * cf
    final_amount=round(final_amount,2)
    response = {
        'fulfillmentText': '{} {} is {} {}'.format(amount, source_currency, final_amount, target_currency)
    }
    print(final_amount)
    return jsonify(response)

def fetch_conversion_factor(source, target):
    url = "https://currency-conversion-and-exchange-rates.p.rapidapi.com/latest"
    querystring = {"from": source, "to": target}
    headers = {
        "X-RapidAPI-Key": "6ec4a9fc45msh1be2ecc6dfa723ap120397jsna247b9cd0a71",
        "X-RapidAPI-Host": "currency-conversion-and-exchange-rates.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()
    conversion_factor = data['rates'][target]
    print(conversion_factor)
    return conversion_factor

if __name__ == "__main__":
    app.run(debug=True)
