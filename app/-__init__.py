from flask import Flask

from flask_sqlalchemy import SQLAlchemy

from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, FileField
from wtforms.validators import DataRequired

from app import routes, models

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://usuario:contraseña@localhost:5432/mi_base_de_datos'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://neondb_owner:GBYUhV93gPwC@ep-wispy-art-a4rjnsko.us-east-1.aws.neon.tech/neondb?sslmode=require'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Setup console logging
if not app.debug:
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    app.logger.addHandler(stream_handler)

app.logger.setLevel(logging.INFO)
app.logger.info('Flask App startup')