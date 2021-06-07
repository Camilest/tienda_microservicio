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
    pedido_valor = db.Column(db.Integer)
    pedido_cantidad = db.Column(db.Integer)
    pedido_estado = db.Column(db.String(100))
    cliente_id = db.Column(db.Integer)
    domiciliario_id = db.Column(db.Integer)
    producto_id = db.Column(db.Integer)

    def __init__(self, datos):
        self.pedido_valor = datos["valor"]
        self.pedido_cantidad = datos["cantidad"]
        self.pedido_estado = datos["estado"]
        self.cliente_id = datos["clienteId"]
        self.domiciliario_id = datos["domiciliarioId"]
        self.producto_id = datos["productoId"]

@app.route("/")
#@cross_origin
def principal():
    data = pedido.query.all()
    diccionario_pedido = {}
    for d in data:
        p = {"id": d.id,
             "valor" : d.pedido_valor,
             "cantidad" : d.pedido_valor,
             "estado" : d.pedido_estado,
             "clienteId" : d.cliente_id,
             "domiciliarioId" : d.domiciliario_id,
             "productoId" : d.producto_id
            }
        diccionario_pedido[d.id] = p
    return diccionario_pedido

@app.route("/agregarPedido/<nombre>/<int:valor>/<int:cantidad>")
#@cross_origin
def agregar(cantidad, valor, estado, clienteId, domiciliarioId, productoId):
    datos = {
        "cantidad": cantidad,
        "valor": valor,
        "estado": estado,
        "clienteId": clienteId,
        "domiciliarioId": domiciliarioId,
        "productoId": productoId
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
def actualizar(id, cantidad, valor, estado, clienteId, domiciliarioId, productoId):
    p = pedido.query.filter_by(id = id).first()
    p.pedido_valor = valor
    p.pedido_cantidad = cantidad
    p.pedido_estado = estado
    p.cliente_id = clienteId
    p.domiciliario_id = domiciliarioId
    p.producto_Id = productoId
    db.session.commit()
    return redirect(url_for('principal'))

@app.route("/buscarPedido/<int:id>")
#@cross_origin
def buscar(id):
    d = pedido.query.filter_by(id = id).first()
    p = {"id": d.id,
        "valor": d.pedido_valor,
        "cantidad": d.pedido_valor,
        "estado": d.pedido_estado,
        "clienteId": d.cliente_id
    }
    return p

@app.route("/estadoPedido/<init:id>")
#@cross_origin
def estadoPedido(id):
    d = pedido.query.filter_by(id = id).first()
    p = {"id": d.id,
        "valor": d.pedido_valor,
        "cantidad": d.pedido_valor,
        "estado": d.pedido_estado,
        "clienteId": d.cliente_id
    }
    return p

if __name__ == "__main__":
    db.create_all()
    app.run(debug = True)
