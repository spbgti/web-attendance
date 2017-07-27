from flask import Flask
from datetime import datetime, date, time
from requests import get
app = Flask(__name__)


@app.route('/hello')
def hello_world():
    return 'Hello World!'


@app.route('/get_time')
def get_now_datetime():
    s = datetime.today().strftime('%d.%m.%Y %H:%M %A')
    return s


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


@app.route('/epoch_unix_time')
def unix_time():
    n = get(' http://date.jsontest.com/')
    n = n.json()

    sec_year = int(n['date'][6:]) - 1970
    sec_month = int(n['date'][:2]) -1
    sec_day = int(n['date'][3:5]) - 1
    if n['time'][9:] == 'AM' and n['time'][9:] != '12':
        sec_hour = int(n["time"][:2])
    else:
        sec_hour = int(n["time"][:2]) + 12
    sec_minute = int(n['time'][3:5])
    sec_second = int(n['time'][6:8])

    day_in_month = {
        0: 0,
        1: 31,
        2: 59,
        3: 90,
        4: 120,
        5: 151,
        6: 181,
        7: 212,
        8: 243,
        9: 273,
        10: 304,
        11: 334
    }

    sec_second = (((sec_year * 365 + sec_year // 4 + day_in_month[sec_month] + sec_day) * 24 + sec_hour) * 60 + sec_minute) * 60 + sec_second
    return sec_second

app.run()

