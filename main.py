from datetime import datetime, timedelta

from flask import Flask, jsonify, make_response, request
from sqlalchemy.exc import IntegrityError

import api
from models import db, Student, Visit

app = Flask(__name__)
app.register_blueprint(api)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

if __name__ == '__main__':
    app.run()
