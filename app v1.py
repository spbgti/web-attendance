from flask import Flask
from datetime import datetime
from requests import get

app = Flask(__name__)


@app.route('/get_time_from_internet')
def get_now_datetime():
    n = get(' http://date.jsontest.com/')
    n = n.json()
    n = datetime.strptime(n, '%d.%m.%Y %H:%M %A').isoformat()
    return n

app.run()
#Я не знаю работает ли оно, ошибка все там же
