from flask import session, render_template, request, redirect, url_for, flash

from flask_sqlalchemy import SQLAlchemy
from app import app, db
from app.models import Producto

from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, FileField
from wtforms.validators import DataRequired

@app.route('/')
def index():
    productos = Producto.query.all()
    #return render_template('index.html', productos=productos)
    return render_template('products_list.html', productos=productos)
