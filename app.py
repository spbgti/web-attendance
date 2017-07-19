from flask import Flask
from datetime import datetime
app = Flask(__name__)

@app.route('/hello')
def hello_world():
    return 'Hello World!'

@app.route('/get_time')
def get_now_datetime():
    return datetime.now().isoformat

app.run()
