from flask import Flask
app = Flask(__name__)

import view1
import view2

@app.route('/')
@app.route('/index')
def index():
    inform = { 'h1': view1.hello_world(), 'h2': view2.dt()}
    return '''
<html>
  <head>
    <title>Home Page</title>
  </head>
  <body>
    <h1>Text: ''' + inform['h1'] + '''</h1>
    <h2>Time: ''' + inform['h2'] + '''</h2>
  </body>
</html>
'''
