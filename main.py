from flask import Flask

from models import db
from api import api

app = Flask(__name__)
app.register_blueprint(api)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db.init_app(app)

if __name__ == '__main__':
    app.run()
