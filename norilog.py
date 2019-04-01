import json

from datetime import datetime
from flask import Flask,request, render_template,redirect, Markup,escape

application = Flask(__name__)

DATA_FILE = 'norilog.json'


@application.template_filter('nl2br')
def nl2br_filter(s):
    """改行文字を br タグ 置き換える テンプレート フィルター"""
    return escape(s).replace('\n', Markup('<br>'))


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
        # json モジュール　でデータ ベースファイルを開きます
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
        # json モジュールで データ ベースファイルを開きます
        database = json.load(open(DATA_FILE, mode="r", encoding="utf-8"))
    except FileNotFoundError:
        database = []
    return database

@application.route('/')
def index():
    """トップページ
    テンプレート を使用してページを表示します
    記録データを読み込みます
    """
    rides =load_data()
    return render_template('index.html',rides=rides)

if __name__ == '__main__':
    # IPアドレス192.168.33.10 の8000番ポートで アプリケーションを実行
    application.run('192.168.33.10',8000,debug=True)
