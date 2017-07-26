from flask import Flask
from datetime import datetime
app = Flask(__name__)


@app.route('/hello')
def hello_world():
    return 'Hello World!'


@app.route('/get_time')
def get_now_datetime():
    s = datetime.today().strftime('%d.%m.%Y %H:%M %A')
    return s

app.run()

