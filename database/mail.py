from models import db
from flask import Flask

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URL'] = 'sqlite:///test.db'

db.init_app(app)