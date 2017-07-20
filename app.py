from flask import Flask
from datetime import datetime
app = Flask(__name__)


@app.route('/hello')
def hello_world():
    return 'Hello World!'


@app.route('/get_time')
def get_now_datetime():
    s = datetime.strftime(datetime.today(), '%d.%m.%Y %H:%M %A')
    return s

app.run()
#Я не понимаю где проблема в url, тк в теории должно работать, а на деле 404 и хоть убейся
