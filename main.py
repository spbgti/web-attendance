from flask import Flask

from models import db
from api import api
from authentication import auth, login_manager

app = Flask(__name__)
app.register_blueprint(api)
app.register_blueprint(auth)
login_manager.init_app(app)
app.secret_key = "your_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db.init_app(app)

if __name__ == '__main__':
    app.run()
