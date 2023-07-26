from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
import json
from flask_cors import CORS

app = Flask(__name__)
#with open('/etc/config.json') as config_file:
#    config = json.load(config_file)
app.config['SECRET_KEY'] = 'jhgdrmkfsjdhg'#config.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///exp3_localData.db" #config.get('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)

from . import views


if __name__ == '__main__':
    app.run()
