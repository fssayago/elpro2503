from datetime import datetime
from app import db

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(200))	
    precio = db.Column(db.Float, nullable=False)
    existencias = db.Column(db.Integer)
    image = db.Column(db.String(200))

    def __repr__(self):
        return f'<Producto {self.nombre}>'
	
