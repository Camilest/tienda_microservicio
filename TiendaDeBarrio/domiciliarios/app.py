from flask import Flask, url_for, redirect
from flask.helpers import url_for
from werkzeug.utils import redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.config['SQL_ALCHEMY_DATABASE_URI'] = 'sqlite:///domiciliarios.db'
app.config['SECRET_KEY'] = "123"
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

db = SQLAlchemy(app)

class domiciliario(db.Model):
    id = db.Column("domiciliary_id", db.Integer, primary_key = True)
    domiciliario_nombre = db.Column(db.String(100))
    domiciliario_apellido = db.Column(db.Integer)
    domiciliario_cedula = db.Column(db.Integer)
    direccion_cliente_id = db.Column(db.Integer)
    pedido_id = db.Column(db.Integer)

    def __init__(self, datos):
        self.domiciliario_nombre = datos["nombre"]
        self.domiciliario_apellido = datos["apellido"]
        self.domiciliario_cedula = datos["cedula"]
        self.direccion_cliente_id = datos["direccionId"]
        self.pedido_id = datos["pedidoId"]

@app.route("/")
#@cross_origin
def principal():
    data = domiciliario.query.all()
    diccionario_domiciliarios = {}
    for d in data:
        p = {"id": d.id,
             "nombre": d.domiciliario_nombre,
             "apellido": d.domiciliario_apellido,
             "cedula": d.domiciliario_apellido
            }
        diccionario_domiciliarios[d.id] = p
    return diccionario_domiciliarios

@app.route("/agregarDomiciliario/<nombre>/<int:valor>/<int:cantidad>")
#@cross_origin
def agregar(nombre, cantidad, valor):
    datos = {
        "nombre": nombre,
        "apellido": cantidad,
        "cedula": valor
    }
    p = domiciliario(datos)
    db.session.add(p)
    db.session.commit()
    return redirect(url_for('principal'))

@app.route("/eliminarDomiciliario/<int:id>")
#@cross_origin
def eliminar(id):
    p = domiciliario.query.filter_by(id = id).first()
    db.session.delete(p)
    db.session.commit()
    return redirect(url_for('principal'))

@app.route("/actualizarDomiciliario/<int:id>/<nombre>/<int:valor>/<int:cantidad>")
#@cross_origin
def actualizar(id, nombre, cantidad, valor):
    p = domiciliario.query.filter_by(id = id).first()
    p.domiciliario_nombre = nombre
    p.domiciliario_apellido = valor
    p.domiciliario_cedula = cantidad
    db.session.commit()
    return redirect(url_for('principal'))

@app.route("/buscarDomiciliario/<int:id>")
#@cross_origin
def buscar(id):
    d = domiciliario.query.filter_by(id = id).first()
    p = {"id": d.id,
        "nombre": d.domiciliario_nombre,
        "apellido": d.domiciliario_apellido,
        "cedula": d.domiciliario_apellido
    }
    return p

if __name__ == "__main__":
    db.create_all()
    app.run(debug = True)
