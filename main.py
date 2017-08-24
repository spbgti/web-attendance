from flask import Flask

import api
from models import db

app = Flask(__name__)
app.register_blueprint(api)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db.init_app(app)

if __name__ == '__main__':
    app.run()
