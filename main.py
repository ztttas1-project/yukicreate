from flask import Flask, request, render_template
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    domain = request.form['domain']
    url = "https://api.render.com/v1/services/srv-cohmstol5elc73cql8g0/custom-domains"
    
    payload = { "name": domain }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": "Bearer rnd_1WAbxx4iZFcBPJlkNTiLeLLE2R1z"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    return response.text

if __name__ == '__main__':
    app.run(port=8080)
