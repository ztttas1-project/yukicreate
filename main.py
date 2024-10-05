from flask import Flask, request, render_template
import requests
import os
import re

app = Flask(__name__)

# ドメイン名の正規表現
DOMAIN_REGEX = r'^(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    domain = request.form['domain']
    
    # ドメイン名の検証
    if not re.match(DOMAIN_REGEX, domain):
        return {"error": "無効なドメイン名です。"}, 400  # 400 Bad Request

    url = "https://api.render.com/v1/services/srv-cohmstol5elc73cql8g0/custom-domains"
    
    payload = {"name": domain}
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {os.getenv('RENDER_API_KEY')}"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # ステータスコードが4xxや5xxの場合に例外を発生させる
        return response.json()  # JSONレスポンスを返す
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}, 500  # エラーメッセージを返す

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))  # 環境変数PORTを取得し、デフォルトは8080
    app.run(host='0.0.0.0', port=port, debug=False)  # 0.0.0.0でバインドして実行
