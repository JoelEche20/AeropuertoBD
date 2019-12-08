from flask import Flask, render_template,request,redirect,url_for 
from bson import ObjectId
from pymongo import MongoClient
import os
import sys

app = Flask(__name__)

title = "Aeropuerto con MongoDB"
heading = "Flask y MongoDB"

client = MongoClient("mongodb://127.0.0.1:27017") 
db = client.mymongodb
vuelos = db.vuelos
reservas = db.reserva

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

@app.route("/")
def index ():
    return render_template('index.html')

@app.route("/vuelos",methods=['GET'])
def mostraVuelos ():
        vuelos_l = vuelos.find()
        return render_template('vuelos.html',vuelos=vuelos_l)

@app.route("/mostrarVuelo",methods = ['POST', 'GET'])
def mostrarVuelo ():
        id=request.values.get("_id")
        vuel=vuelos.find({"_id":ObjectId(id)})
        return render_template('reserva.html',vuelos=vuel)

@app.route("/reservas")
def viewReservas ():
    return 'hola'

@app.route("/completarReserva",methods=['POST'])
def completarReserva():
        if request.method == 'POST':
                id = request.values.get('idVuel')
                id_vuelo = request.values.get('id_vuelo')
                nombre = request.values.get('nombre')
                id_asiento= request.values.get('id_asiento')
                reservas.insert({"id_vuelo":id_vuelo,"nombre":nombre, "id_asiento":id_asiento})      
                vuelos.update({"_id":ObjectId(id),"asientos.id_asiento":id_asiento},{"$set":{"asientos.$.estado":False}})
                return  redirect(url_for('index'))


if __name__ == "__main__":
    app.run(port=3000, debug=True)
