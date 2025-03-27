from flask import session, render_template, request, redirect, url_for, flash

from flask_sqlalchemy import SQLAlchemy
from app import app, db
from app.models import Producto

from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, FileField
from wtforms.validators import DataRequired

@app.route('/')
def product_list():
    productos = Producto.query.all()
    #return render_template('index.html', productos=productos)
    return render_template('products_list.html', productos=productos)

@app.route('/empty')
def empty_cart():
    try:
        session.clear()
        return redirect(url_for('.product_list'))
    except Exception as e:
        print(e)	

@app.route('/add', methods=['POST'])
def add_product_to_cart():
    _id = request.form['id']	
    _nombre = request.form['nombre']
    _descripcion = request.form['descripcion']		
    _precio = request.form['precio']
    _cantidad = int(request.form['cantidad'])	
    _existencias = int(request.form['existencias'])	
    _image = request.form['image']	

    # validate the received values
    if _cantidad and _id and request.method == 'POST':
		#_item = db.session.execute(select(Subscription).filter_by(id)).scalar_one()
		#_item = db.session.execute(db.select(Subscription).order_by(Subscription.id)).scalars()
        #_item = db.session.execute(select(Subscription).where(id == 1)).scalar_one()
        _item = db.session.execute(db.select(Producto).where(id==1)).scalars()
        #_item = db.session.execute("SELECT * FROM Subscription WHERE id=:_id", {"_id": _id})
        #names = [row[0] for row in _item]
        itemArray = { _id : {'nombre' : _nombre, 'id' : _id, 'cantidad' : _cantidad, 'existencias' : _existencias, 'precio' : _precio, 'image' : _image, 'precio_total': int(_cantidad) * float(_precio)}}
        t_precio_total = 0
        t_cantidad_total = 0
        session.modified = True
		
        if 'carro_item' in session:
            if _id in session['carro_item']:
                for key, value in session['carro_item'].items():
                    if _id == key:
                        a_cantidad = session['carro_item'][key]['cantidad']
                        total_cantidad = int(a_cantidad) + int(_cantidad)
                        session['carro_item'][key]['cantidad'] = total_cantidad
                        session['carro_item'][key]['precio_total'] = int(total_cantidad) * float(_precio)
            else:
                session['carro_item'] = array_merge(session['carro_item'], itemArray)
         
            for key, value in session['carro_item'].items():
                i_cantidad = int(session['carro_item'][key]['cantidad'])
                i_precio = float(session['carro_item'][key]['precio_total'])
                t_cantidad_total = int(t_cantidad_total) + int(i_cantidad)
                t_precio_total = int(t_precio_total) + float(i_precio)
        else:
            session['carro_item'] = itemArray
            t_cantidad_total = int(t_cantidad_total) + int(_cantidad)
            t_precio_total = int(t_precio_total) + int(_cantidad) * float(_precio)
             
        session['t_cantidad_total'] = t_cantidad_total
        session['t_precio_total'] = t_precio_total

        #flash(itemArray, 'success')
        return redirect(url_for('product_list'))
    else:
        return 'Error while adding item to cart'	
		
@app.route('/delete/<string:id>')
def delete_product(id):
    try:
        t_precio_total = 0
        t_cantidad_total = 0
        session.modified = True
         
        for item in session['carro_item'].items():
            if item[0] == id:    
                session['carro_item'].pop(item[0], None)
                if 'carro_item' in session:
                    for key, value in session['carro_item'].items():
                        i_cantidad = int(session['carro_item'][key]['cantidad'])
                        i_precio = float(session['carro_item'][key]['precio_total'])
                        t_cantidad_total = t_cantidad_total + i_cantidad
                        t_precio_total = t_precio_total + i_precio
                break
         
        if t_cantidad_total == 0:
            session.clear()
        else:
            session['t_cantidad_total'] = t_cantidad_total
            session['t_precio_total'] = t_precio_total
    
        flash('Borrado successful!!', 'success')
        return redirect(url_for('product_list'))             
    except Exception as e:
        print(e)
	
def array_merge( first_array , second_array ):
    if isinstance( first_array , list ) and isinstance( second_array , list ):
        return first_array + second_array
    elif isinstance( first_array , dict ) and isinstance( second_array , dict ):
        return dict( list( first_array.items() ) + list( second_array.items() ) )
    elif isinstance( first_array , set ) and isinstance( second_array , set ):
        return first_array.union( second_array )
    return False
	
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
