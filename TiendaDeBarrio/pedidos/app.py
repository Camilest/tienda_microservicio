from flask import Flask, url_for, redirect
from flask.helpers import url_for
from werkzeug.utils import redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.config['SQL_ALCHEMY_DATABASE_URI'] = 'sqlite:///orders.db'
app.config['SECRET_KEY'] = "123"
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

db = SQLAlchemy(app)

class pedido(db.Model):
    id = db.Column("order_id", db.Integer, primary_key = True)
    pedido_nombre = db.Column(db.String(100))
    pedido_valor = db.Column(db.Integer)
    pedido_cantidad = db.Column(db.Integer)

    def __init__(self, datos):
        self.pedido_nombre = datos["nombre"]
        self.pedido_valor = datos["valor"]
        self.pedido_cantidad = datos["cantidad"]

@app.route("/")
#@cross_origin
def principal():
    data = pedido.query.all()
    diccionario_productos = {}
    for d in data:
        p = {"id": d.id,
             "nombre": d.pedido_nombre,
             "valor": d.pedido_valor,
             "cantidad": d.pedido_valor
            }
        diccionario_productos[d.id] = p
    return diccionario_productos

@app.route("/agregarPedido/<nombre>/<int:valor>/<int:cantidad>")
#@cross_origin
def agregar(nombre, cantidad, valor):
    datos = {
        "nombre": nombre,
        "cantidad": cantidad,
        "valor": valor
    }
    p = pedido(datos)
    db.session.add(p)
    db.session.commit()
    return redirect(url_for('principal'))

@app.route("/eliminarPedido/<int:id>")
#@cross_origin
def eliminar(id):
    p = pedido.query.filter_by(id = id).first()
    db.session.delete(p)
    db.session.commit()
    return redirect(url_for('principal'))

@app.route("/actualizarPedido/<int:id>/<nombre>/<int:valor>/<int:cantidad>")
#@cross_origin
def actualizar(id, nombre, cantidad, valor):
    p = pedido.query.filter_by(id = id).first()
    p.pedido_nombre = nombre
    p.pedido_valor = valor
    p.pedido_cantidad = cantidad
    db.session.commit()
    return redirect(url_for('principal'))

@app.route("/buscarPedido/<int:id>")
#@cross_origin
def buscar(id):
    d = pedido.query.filter_by(id = id).first()
    p = {"id": d.id,
        "nombre": d.pedido_nombre,
        "valor": d.pedido_valor,
        "cantidad": d.pedido_valor
    }
    return p

if __name__ == "__main__":
    db.create_all()
    app.run(debug = True)
