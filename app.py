from flask import Flask
app = Flask(__name__)

def hello_world():
    return 'Hello World!'

from datetime import datetime
def get_now_datetime():
    return datetime.now().isoformat

@app.route('/')
# @app.route('/index')
def index():
    'Текст:{}\n Время:{}'.format(hello_world(), get_now_datetime())

app.run()
