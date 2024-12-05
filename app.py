from flask import Flask, jsonify, render_template
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

#1. ofertas y promociones
@app.route("/ofertas", methods=["GET"])
def ofertasPromociones():
    ofertas= [
        {"nombre":"pulpa de guayaba", "descuento": "20%"},
        {"nombre":"chocolate corona", "descuento": "50%"},
        {"nombre":"arroz diana", "descuento": "15%"}
    ]
    return jsonify(ofertas)

#2.cátalogo de productos
@app.route("/catalogo", methods=["GET"])
def Catalogo():
    productos= [
        {"id":1,"nombre":"pulpa de guayaba", "precio": 5000},
        {"id":2,"nombre":"chocolate corona", "precio": 8000},
        {"id":3,"nombre":"arroz diana", "precio": 2500}
    ]
    return jsonify(productos)

#3.detalle de productos
@app.route("/detalle/<init:id>", methods=["GET"])
def detalleProducto(id):
    producto= {"id":id,"nombre":f"Producto {id}", "descripcion":"descripción del producto","precio".100 * id}
    return jsonify(producto)

#4.detalle de envio
@app.route("/detalleE", methods=["GET"])
def detalleEnvio():
    envio= {"metodo":"envío estandar", "costo": 11000, "tiempoEstimado": "3-5 días"}
    return jsonify(envio)

#5. pagos con metodo
@app.route("/pago", methods=["POST"])
def procesarPago():
    data= request.json()
    metodoPago = data.get("metodoPago", "No identificado")
    return jsonify({"mensaje":f"Pago de proceso con:{metodoPago}"}) 

#6. búsqueda avanzada
@app.route("/busqueda", methods=["GET"])
def busquedaAvanzada():
    query = request.args.get("query","")
    busqueda = [{"producto": "pulpa de guayaba", "precio": 5000}, 
                {"producto": "chocolate corona", "precio": 8000}, 
                {"producto": "arroz diana", "precio": 2500}]
    return jsonify(busqueda)

#7.soporte
# Almacén de agentes disponibles
agentes = ["Agente 1", "Agente 2"]

@socketio.on("connect")
def handle_connect():
    print("Usuario conectado")

@socketio.on("disconnect")
def handle_disconnect():
    print("Usuario desconectado")

@socketio.on("message")
def handle_message(data):
    print(f"Mensaje recibido: {data}")
    respuesta = {
        "usuario": data["usuario"],
        "mensaje": data["mensaje"],
        "respuesta": f"{agentes[0]} dice: Estoy aquí para ayudarte con '{data['mensaje']}'"
    }
    emit("respuesta", respuesta, broadcast=True)

if _name_ == '_main_':
    socketio.run(app, debug=True)
if __name__ == "__main__":
    app.run(debug=True)