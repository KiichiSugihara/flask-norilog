import json
from datetime import datetime
from flask import Flask, render_template,redirect

application = Flask(__name__)

DATA_FILE = 'norilog.json'

# 記録データを jsonに保存する
def save_data(start, finish, memo, create_at):
    """記録データを保存します
    :param start: 乗った駅
    :type start: str
    :param finish: 降りた駅
    :type finish: str
    :param memo: 乗り降りのメモ
    :type memo: str
    :param create_at: 乗り降りの日付
    :type create_at: datetime.datetime
    :return: None
    """
    try:
        # json モジュール　でデータベースファイルを開きます
        database = json.load(open(DATA_FILE, mode="r", encoding="utf-8"))
    except FileNotFoundError:
        database = []

    database.insert(0, {
        "start": start,
        "finish": finish,
        "memo": memo,
        "create_at": create_at.strftime("%Y-%m-%d %H:%M")
    })

    json.dump(database, open(DATA_FILE, mode="w", encoding="utf-8"), indent=4, ensure_ascii=False)

@application.route('/save', methods=['POST'])
def save():
    """記録用"""
    start = request.form.get('start')
    finish = request.form.get('finish')
    memo = request.form.get('memo')
    create_at = datetime.now()
    save_data(start, finish, memo, create_at)
    return redirect('/')

def load_data():
    """記録データを返します"""
    try:
        # json モジュールでデータベースファイルを開きます
        database = json.load(open(DATA_FILE, mode="r", encoding="utf-8"))
    except FileNotFoundError:
        database = []
    return database

@application.route('/')
def index():
    """トップページ
    テンプレートを使用してページを表示します
    記録データを読み込みます
    """
    rides =load_data()
    return render_template('index.html',rides=rides)

if __name__ == '__main__':
    # IPアドレス0.0.0.0 の8000番ポートでアプリケーションを実行
    application.run('0.0.0.0',8000,debug=True)
