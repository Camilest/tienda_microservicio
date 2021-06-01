from flask import Flask , url_for, redirect
from flask.helpers import url_for
from werkzeug.utils import redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin

aap = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///productos.db'
app.config['SECRET_KEY'] = "123"

db = SQLAlchemy(app)

class producto(db.Model):
    id = db.Column("product_id", db.Integer, primary_key = True)
    producto_nombre = db.Column(db.String(100))
    producto_valor = db.Column(db.Integer)
    producto_cantidad = db.Column(db.Integer)

    def __init__(self, datos):
        self.producto_nombre = datos["nombre"]
        self.producto_valor = datos["valor"]
        self.producto_cantidad = datos["cantidad"]

@app.route("/")
def principal():
    data = producto.query.all()
    diccionario_productos = {}
    for d in data:
        p = {"id": d.id,
             "nombre": d.producto_nombre,
             "valor": d.producto_valor,
             "cantidad": d.producto_valor
            }
        diccionario_productos[d.id] = p
    return diccionario_productos

@app.router("/agregar/<nombre>/<int:valor/<int:cantidad>")
def agregar(nombre, cantidad, valor):
    datos = {
        "nombre": nombre,
        "cantidad": cantidad,
        "valor": valor
    }
    p = producto(datos)
    db.session.add(p)
    db.session.commit()
    return redirect(url_for('principal'))

@app.route("/eliminar/<int:id>")
def eliminar(id):
    p = producto.query.filter_by(id = id).first()
    db.session.delete(p)
    db.session.commit()
    return redirect(url_for('principal'))

@app.router("/actualizar/<int:id>/<nombre>/<int:valor/<int:cantidad>")
def actualizar(id, nombre, cantidad, valor):
    p = producto.query.filter_by(id = id).first()
    p.producto_nombre = nombre
    p.producto_valor = valor
    p.producto_cantidad = cantidad
    db.session.commit()
    return redirect(url_for('principal'))

@app.route("/buscar/<int:id>")
def buscar(id):
    d = producto.query.filter_by(id = id).first()
    p = {"id": d.id,
        "nombre": d.producto_nombre,
        "valor": d.producto_valor,
        "cantidad": d.producto_valor
    }
    return p

if __name__ == "__main__":
    db.create_all()
    db.run(debug = True)