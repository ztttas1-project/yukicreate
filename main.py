from flask import Flask, request, render_template
import requests
import os
import re
import schedule
import time
import threading
import random
import string
app = Flask(__name__)
key = ""
# ドメイン名の正規表現
DOMAIN_REGEX = r'^(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$'
serid = ""

# Render APIのエンドポイント
from flask import Flask, request, render_template
import requests
import os
import re
import schedule
import time
import threading
import random
import string
app = Flask(__name__)
key = ""
# ドメイン名の正規表現
DOMAIN_REGEX = r'^(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$'
serid = ""

# Render APIのエンドポイント

# ホワイトリスト
whitelist = ["easterndns.com", "ydns.eu","ipv64.net","ipv64.de","any64.de","api64.de","dns64.de","dyndns64.de","dynipv6.de","eth64.de","home64.de","iot64.de","lan64.de","nas64.de","root64.de","route64.de","srv64.de","tcp64.de","udp64.de","vpn64.de","wan64.de","calculator123456789.store"]
def generate_random_string(length=15):
    characters = string.ascii_letters + string.digits  # アルファベットと数字
    return ''.join(random.choice(characters) for _ in range(length))
def fetch_custom_domains():
    try:
        response = requests.get(BASE_URL, headers=HEADERS)
        response.raise_for_status()
        return response.json()  # JSONレスポンスを返す
    except requests.exceptions.RequestException as e:
        print(f"ドメインの取得中にエラーが発生しました: {e}")
        return []

def delete_custom_domain(domain_id):
    try:
        response = requests.delete(f"{BASE_URL}/{domain_id}", headers=HEADERS)
        response.raise_for_status()
        print(f"ドメイン {domain_id} を削除しました。")
    except requests.exceptions.RequestException as e:
        print(f"ドメインの削除中にエラーが発生しました: {e}")

def check_and_delete_invalid_domains():
    domains = fetch_custom_domains()
    for domain in domains:
        if not domain['isVerified']:  # 認証されていないドメイン
            delete_custom_domain(domain['id'])

# スケジュール設定
def run_scheduler():
    schedule.every(10).minutes.do(check_and_delete_invalid_domains)  # 10分ごとに実行

    while True:
        schedule.run_pending()
        time.sleep(1)
domainf5 = "yukimod"
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/submit2', methods=['POST'])
def submit2():
    # ランダムな文字列を生成
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=15))
    
    # Renderに登録するドメイン名
    domain_name = f"{random_string}.{domainf5}.f5.si"
    
    # Render APIにPOSTリクエストを送信
    response = add_custom_domain(domain_name)
    
    if response.status_code == 200:
        return f"message: Domain registered successfully, domain: {domain_name}", 200
    else:
        return f"message: Failed to register domain, error: {response.text}", 400

def add_custom_domain(domain):
    # RenderのAPIキーを設定
    api_key = os.environ['KEY2']  # APIキーを自分のものに置き換えてください
    service_id = "srv-comtq2a1hbls73f9a3d0"  # 対象のサービスIDを指定
    
    url = f"https://api.render.com/v1/services/{service_id}/custom-domains"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "domain": domain
    }
    
    # POSTリクエストを送信
    return requests.post(url, headers=headers, json=data)
@app.route('/submit', methods=['POST'])
def submit():
    domain = request.form['domain']
    server_choice = request.form['server']  # 選択されたサーバーを取得
    
    # ドメイン名の検証
    if not re.match(DOMAIN_REGEX, domain):
        return {"error": "Invalid domain name."}, 400  # 400 Bad Request

    # ホワイトリストのチェック
    if not any(domain.endswith(whitelisted) for whitelisted in whitelist):
        return {"error": "The domain is not included in the whitelist."}, 400  # 400 Bad Request

    payload = {"name": domain}
    # サーバーに応じた設定
    if server_choice == "1":
        key = os.environ['KEY1']
        serid = "srv-cohmstol5elc73cql8g0"
    elif server_choice == "2":
        key = os.environ['KEY2']
        serid = "srv-comtq2a1hbls73f9a3d0"
    elif server_choice == "3":
        key = os.environ['KEY3']
        serid = "srv-crkkbvrv2p9s73e36tp0"
    elif server_choice == "4":
        key = os.environ['KEY4']
        serid = "srv-cs7n565umphs73a9lpsg"
    else:
        return {"error": "Invalid server choice."}, 400  # 400 Bad Request
    
    BASE_URL = f"https://api.render.com/v1/services/{serid}/custom-domains"
    HEADERS = {"accept": "application/json","content-type": "application/json","authorization": f"Bearer {key}"}
    
    try:
        response = requests.post(BASE_URL, json=payload, headers=HEADERS)
        response.raise_for_status()  # ステータスコードが4xxや5xxの場合に例外を発生させる
        return response.json()  # JSONレスポンスを返す
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}, 500  # エラーメッセージを返す
    #if ser == 1:
    #    key = os.environ['KEY1']
    #    serid = "srv-cohmstol5elc73cql8g0"
    #    try:
    #        response = requests.post(BASE_URL, json=payload, headers=HEADERS)
    #        response.raise_for_status()  # ステータスコードが4xxや5xxの場合に例外を発生させる
    #        return response.json()  # JSONレスポンスを返す
    #    except requests.exceptions.RequestException as e:
    #        return {"error": str(e)}, 500  # エラーメッセージを返す
    #elif ser == 2:
    #    key = os.environ['KEY2']
    #    serid = "srv-comtq2a1hbls73f9a3d0"
    #    try:
    #        response = requests.post(BASE_URL, json=payload, headers=HEADERS)
    #        response.raise_for_status()  # ステータスコードが4xxや5xxの場合に例外を発生させる
    #        return response.json()  # JSONレスポンスを返す
    #    except requests.exceptions.RequestException as e:
    #        return {"error": str(e)}, 500  # エラーメッセージを返す
    #elif ser == 3:
    #    key = os.environ['KEY3']
    #    serid = "srv-crkkbvrv2p9s73e36tp0"
    #    try:
    #        response = requests.post(BASE_URL, json=payload, headers=HEADERS)
    #        response.raise_for_status()  # ステータスコードが4xxや5xxの場合に例外を発生させる
    #        return response.json()  # JSONレスポンスを返す
    #    except requests.exceptions.RequestException as e:
    #        return {"error": str(e)}, 500  # エラーメッセージを返す
if __name__ == '__main__':
    # スケジューラースレッドを開始
    threading.Thread(target=run_scheduler, daemon=True).start()
    
    port = int(os.getenv('PORT', 8080))  # 環境変数PORTを取得し、デフォルトは8080
    app.run(host='0.0.0.0', port=port, debug=False)  # 0.0.0.0でバインドして実行
# ホワイトリスト
whitelist = ["easterndns.com", "ydns.eu","ipv64.net","ipv64.de","any64.de","api64.de","dns64.de","dyndns64.de","dynipv6.de","eth64.de","home64.de","iot64.de","lan64.de","nas64.de","root64.de","route64.de","srv64.de","tcp64.de","udp64.de","vpn64.de","wan64.de","calculator123456789.store"]
def generate_random_string(length=15):
    characters = string.ascii_letters + string.digits  # アルファベットと数字
    return ''.join(random.choice(characters) for _ in range(length))
def fetch_custom_domains():
    try:
        response = requests.get(BASE_URL, headers=HEADERS)
        response.raise_for_status()
        return response.json()  # JSONレスポンスを返す
    except requests.exceptions.RequestException as e:
        print(f"ドメインの取得中にエラーが発生しました: {e}")
        return []

def delete_custom_domain(domain_id):
    try:
        response = requests.delete(f"{BASE_URL}/{domain_id}", headers=HEADERS)
        response.raise_for_status()
        print(f"ドメイン {domain_id} を削除しました。")
    except requests.exceptions.RequestException as e:
        print(f"ドメインの削除中にエラーが発生しました: {e}")

def check_and_delete_invalid_domains():
    domains = fetch_custom_domains()
    for domain in domains:
        if not domain['isVerified']:  # 認証されていないドメイン
            delete_custom_domain(domain['id'])

# スケジュール設定
def run_scheduler():
    schedule.every(10).minutes.do(check_and_delete_invalid_domains)  # 10分ごとに実行

    while True:
        schedule.run_pending()
        time.sleep(1)
domainf5 = "yukimod"
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/submit2', methods=['POST'])
def submit2():
    # ランダムな文字列を生成
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=15))
    
    # Renderに登録するドメイン名
    domain_name = f"{random_string}.{domainf5}.f5.si"
    
    # Render APIにPOSTリクエストを送信
    response = add_custom_domain(domain_name)
    
    if response.status_code == 201:
        return f"message: Domain registered successfully, domain: {domain_name}", 200
    else:
        return f"message: Failed to register domain, error: {response.text}", 400

def add_custom_domain(domain):
    # RenderのAPIキーを設定
    api_key = os.environ['KEY2']  # APIキーを自分のものに置き換えてください
    service_id = "srv-crkkbvrv2p9s73e36tp0"  # 対象のサービスIDを指定
    
    url = f"https://api.render.com/v1/services/{service_id}/custom-domains"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "domain": domain
    }
    
    # POSTリクエストを送信
    return requests.post(url, headers=headers, json=data)
@app.route('/submit', methods=['POST'])
def submit():
    domain = request.form['domain']
    server_choice = request.form['server']  # 選択されたサーバーを取得
    
    # ドメイン名の検証
    if not re.match(DOMAIN_REGEX, domain):
        return {"error": "Invalid domain name."}, 400  # 400 Bad Request

    # ホワイトリストのチェック
    if not any(domain.endswith(whitelisted) for whitelisted in whitelist):
        return {"error": "The domain is not included in the whitelist."}, 400  # 400 Bad Request

    payload = {"name": domain}
    # サーバーに応じた設定
    if server_choice == "1":
        key = os.environ['KEY1']
        serid = "srv-cohmstol5elc73cql8g0"
    elif server_choice == "2":
        key = os.environ['KEY2']
        serid = "srv-comtq2a1hbls73f9a3d0"
    elif server_choice == "3":
        key = os.environ['KEY3']
        serid = "srv-crkkbvrv2p9s73e36tp0"
    elif server_choice == "4":
        key = os.environ['KEY4']
        serid = "srv-cs7n565umphs73a9lpsg"
    else:
        return {"error": "Invalid server choice."}, 400  # 400 Bad Request
    
    BASE_URL = f"https://api.render.com/v1/services/{serid}/custom-domains"
    HEADERS = {"accept": "application/json","content-type": "application/json","authorization": f"Bearer {key}"}
    
    try:
        response = requests.post(BASE_URL, json=payload, headers=HEADERS)
        response.raise_for_status()  # ステータスコードが4xxや5xxの場合に例外を発生させる
        return response.json()  # JSONレスポンスを返す
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}, 500  # エラーメッセージを返す
    #if ser == 1:
    #    key = os.environ['KEY1']
    #    serid = "srv-cohmstol5elc73cql8g0"
    #    try:
    #        response = requests.post(BASE_URL, json=payload, headers=HEADERS)
    #        response.raise_for_status()  # ステータスコードが4xxや5xxの場合に例外を発生させる
    #        return response.json()  # JSONレスポンスを返す
    #    except requests.exceptions.RequestException as e:
    #        return {"error": str(e)}, 500  # エラーメッセージを返す
    #elif ser == 2:
    #    key = os.environ['KEY2']
    #    serid = "srv-comtq2a1hbls73f9a3d0"
    #    try:
    #        response = requests.post(BASE_URL, json=payload, headers=HEADERS)
    #        response.raise_for_status()  # ステータスコードが4xxや5xxの場合に例外を発生させる
    #        return response.json()  # JSONレスポンスを返す
    #    except requests.exceptions.RequestException as e:
    #        return {"error": str(e)}, 500  # エラーメッセージを返す
    #elif ser == 3:
    #    key = os.environ['KEY3']
    #    serid = "srv-crkkbvrv2p9s73e36tp0"
    #    try:
    #        response = requests.post(BASE_URL, json=payload, headers=HEADERS)
    #        response.raise_for_status()  # ステータスコードが4xxや5xxの場合に例外を発生させる
    #        return response.json()  # JSONレスポンスを返す
    #    except requests.exceptions.RequestException as e:
    #        return {"error": str(e)}, 500  # エラーメッセージを返す
if __name__ == '__main__':
    # スケジューラースレッドを開始
    threading.Thread(target=run_scheduler, daemon=True).start()
    
    port = int(os.getenv('PORT', 8080))  # 環境変数PORTを取得し、デフォルトは8080
    app.run(host='0.0.0.0', port=port, debug=False)  # 0.0.0.0でバインドして実行
