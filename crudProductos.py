#¡Claro! Aquí tienes un ejemplo de cómo implementar un CRUD (Crear, Leer, Actualizar, Eliminar) para una tabla de productos utilizando Flask, SQLAlchemy y PostgreSQL. Este ejemplo también emplea request.form para manejar los datos del formulario.

#Configuración Inicial

#Primero, asegúrate de tener Flask y SQLAlchemy instalados:

#Copy the code
#pip install Flask Flask-SQLAlchemy psycopg2-binary

#Estructura del Proyecto

Tu proyecto podría tener la siguiente estructura:

Copy the code
/mi_proyecto
    /app
        __init__.py
        models.py
        routes.py
    run.py

__init__.py

Configura tu aplicación Flask y SQLAlchemy:

Copy the code
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://usuario:contraseña@localhost:5432/mi_base_de_datos'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from app import routes

models.py

Define el modelo de tu tabla de productos:

Copy the code
from app import db

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    descripcion = db.Column(db.String(200))

    def __repr__(self):
        return f'<Producto {self.nombre}>'

routes.py

Implementa las rutas para el CRUD:

Copy the code
from flask import render_template, request, redirect, url_for
from app import app, db
from app.models import Producto

@app.route('/')
def index():
    productos = Producto.query.all()
    return render_template('index.html', productos=productos)

@app.route('/producto/nuevo', methods=['GET', 'POST'])
def nuevo_producto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = request.form['precio']
        descripcion = request.form['descripcion']
        
        nuevo_producto = Producto(nombre=nombre, precio=precio, descripcion=descripcion)
        db.session.add(nuevo_producto)
        db.session.commit()
        
        return redirect(url_for('index'))
    return render_template('nuevo_producto.html')

@app.route('/producto/editar/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    producto = Producto.query.get_or_404(id)
    if request.method == 'POST':
        producto.nombre = request.form['nombre']
        producto.precio = request.form['precio']
        producto.descripcion = request.form['descripcion']
        
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('editar_producto.html', producto=producto)

@app.route('/producto/eliminar/<int:id>', methods=['POST'])
def eliminar_producto(id):
    producto = Producto.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()
    return redirect(url_for('index'))

run.py

Ejecuta tu aplicación Flask:

Copy the code
from app import app

if __name__ == '__main__':
    app.run(debug=True)

Plantillas HTML
index.html
Copy the code
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Productos</title>
</head>
<body>
    <h1>Lista de Productos</h1>
    <a href="{{ url_for('nuevo_producto') }}">Nuevo Producto</a>
    <ul>
        {% for producto in productos %}
            <li>{{ producto.nombre }} - {{ producto.precio }} - {{ producto.descripcion }}
                <a href="{{ url_for('editar_producto', id=producto.id) }}">Editar</a>
                <form action="{{ url_for('eliminar_producto', id=producto.id) }}" method="post" style="display:inline;">
                    <button type="submit">Eliminar</button>
                </form>
            </li>
        {% endfor %}
    </ul>
</body>
</html>

nuevo_producto.html
Copy the code
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Nuevo Producto</title>
</head>
<body>
    <h1>Nuevo Producto</h1>
    <form action="{{ url_for('nuevo_producto') }}" method="post">
        <label for="nombre">Nombre:</label>
        <input type="text" id="nombre" name="nombre"><br>
        <label for="precio">Precio:</label>
        <input type="text" id="precio" name="precio"><br>
        <label for="descripcion">Descripción:</label