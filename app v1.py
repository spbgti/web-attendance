from flask import Flask
from datetime import datetime, date, time
from requests import get

app = Flask(__name__)


@app.route('/get_time_from_internet')
def get_now_datetime():
    n = get(' http://date.jsontest.com/')
    n = n.json()
    s_date = date(int(n['date'][6:]), int(n['date'][:2]), int(n['date'][3:5]))
    if n['time'][9:] == 'AM' and n['time'][9:] != '12':
        s_time = time(int(n["time"][:2]), int(n['time'][3:5]), int(n['time'][6:8]))
    else:
        s_time = time(int(n["time"][:2]) + 12, int(n['time'][3:5]), int(n['time'][6:8]))
    s_date_time = datetime.combine(s_date, s_time)
    return s_date_time.isoformat()

app.run()
