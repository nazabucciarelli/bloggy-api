from flask import Flask
import os

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from dotenv import load_dotenv
from flask_marshmallow import Marshmallow

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DB_URI')
app.config['JWT_SECRET_KEY']=os.environ.get('JWT_SECRET_KEY')

db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)

from app.views import view

