from flask import Flask, render_template,request,redirect,url_for 
from bson import ObjectId
from pymongo import MongoClient
from datetime import datetime
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

@app.route("/misReservas")
def misReservas ():
    return render_template('misReservas.html')


@app.route("/delete",methods = ['POST', 'GET'])
def delete ():
        key=request.values.get("idR")
        idVuelo=request.values.get("idVuelo")
        idAsiento=request.values.get("idA")
        eprint(idAsiento)
        vuelos.update({"_id":ObjectId(idVuelo),"asientos.id_asiento":idAsiento},{"$set":{"asientos.$.estado":True}})
        reservas.remove({"_id":ObjectId(key)})
        return render_template('misReservas.html')

@app.route("/searchD")
def searchD ():
    return render_template('searchDate.html')

@app.route("/searchDate",methods = ['POST', 'GET'])
def searchDate ():
        date =request.values.get('query')
        vuelos_S=vuelos.find({"fecha":date})
        return render_template('searchDate.html',vuelos=vuelos_S)

@app.route("/searchMyReserv",methods = ['POST', 'GET'])
def searchMyReserv ():
        misReservas=[]
        nombre =request.values.get('query')
        res=reservas.find({"nombre":nombre})
        exist=False

        for r in res:
                vuelo = vuelos.find({"cod_vuelo":r["id_vuelo"]})[0]
                misReservas.append({"vuelo": vuelo, "r": r})
        
        if misReservas != []:
                exist=True
        return render_template('misReservas.html',reservas=misReservas,exist=exist,name=nombre)

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
