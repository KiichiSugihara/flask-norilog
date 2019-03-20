import json

from flask import Flask, render_template

application = Flask(__name__)

DATA_FILE = 'norilog.json'


def save_data(start, finish, memo, created_at):
    """記録データを保存します
    """
    # 省略


def load_data():
    """投稿されたデータを返します
    """
    # 省略

@application.route('/')
def index():
    """トップページ
    テンプレートを使用してページを表示します
    """
    return render_template('index.html')


if __name__ == '__main__':
    # IPアドレス0.0.0.0の8000番ポートでアプリケーションを実行します
    application.run('0.0.0.0', 8000, debug=True)
