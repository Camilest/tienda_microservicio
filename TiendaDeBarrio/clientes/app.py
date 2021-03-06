from flask import Flask, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.config['SQL_ALCHEMY_DATABASE_URI'] = 'sqlite:///clientes.db'
app.config['SECRET_KEY'] = "123"
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

db = SQLAlchemy(app)

class cliente(db.Model):
    id = db.Column("client_id", db.Integer, primary_key = True)
    cliente_nombre = db.Column(db.String(100))
    cliente_Apellido = db.Column(db.Integer)
    cliente_Cedula = db.Column(db.Integer)
    cliente_Direccion = db.Column(db.String(100))

    def __init__(self, datos):
        self.cliente_nombre = datos["nombre"]
        self.cliente_Apellido = datos["apellido"]
        self.cliente_Cedula = datos["cedula"]
        self.cliente_Direccion = datos["direccion"]

@app.route("/")
#@cross_origin
def principal():
    data = cliente.query.all()
    diccionario_clientes = {}
    for d in data:
        p = {"id": d.id,
             "nombre": d.cliente_nombre,
             "apellido": d.cliente_Apellido,
             "cedula": d.cliente_Apellido,
             "direccion": d.cliente_Direccion
            }
        diccionario_clientes[d.id] = p
    return diccionario_clientes

@app.route("/agregarCliente/<nombre>/<int:valor>/<int:cantidad>")
#@cross_origin
def agregar(nombre, cantidad, cedula, direccion):
    datos = {
        "nombre": nombre,
        "apellido": cantidad,
        "cedula": cedula,
        "direccion": direccion
    }
    p = cliente(datos)
    db.session.add(p)
    db.session.commit()
    return redirect(url_for('principal'))

@app.route("/eliminarCliente/<int:id>")
#@cross_origin
def eliminar(id):
    p = cliente.query.filter_by(id = id).first()
    db.session.delete(p)
    db.session.commit()
    return redirect(url_for('principal'))

@app.route("/actualizarCliente/<int:id>/<nombre>/<int:valor>/<int:cantidad>")
#@cross_origin
def actualizar(id, nombre, cantidad, cedula, direccion):
    p = cliente.query.filter_by(id = id).first()
    p.cliente_nombre = nombre
    p.cliente_Apellido = cedula
    p.cliente_Cedula = direccion
    db.session.commit()
    return redirect(url_for('principal'))

@app.route("/buscarCliente/<int:id>")
#@cross_origin
def buscar(id):
    d = cliente.query.filter_by(id = id).first()
    p = {"id": d.id,
        "nombre": d.cliente_nombre,
        "apellido": d.cliente_Apellido,
        "cedula": d.cliente_Apellido,
        "direccion": d.cliente_direccion
    }
    return p

if __name__ == "__main__":
    db.create_all()
    app.run(debug = True)
