from flask import request
from flask_restful import Resource
from ..modelos import db, Inicio_de_sesión, Registro, paginaPrincipal, productos, pedidos, envios, carrito, ofertas_y_promociones
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import (
    jwt_required, create_access_token, get_jwt_identity
)
# Esquemas para serializar los datos
Inicio_de_sesión_schema = Inicio_de_sesiónSchema()
Registro_schema = RegistroSchema(many=True)
paginaPrincipal_schema = paginaPrincipalSchema()
productos_schema = productosSchema(many=True)
pedidos_schema = pedidosSchema()
envios_schema = enviosSchema(many=True)
carrito_schema = carrito_Schema()
ofertas_y_promocionesschema = ofertas_y_promocionesSchema(many=True)



import logging

from flask import request
from flask_restful import Resource
from sqlalchemy.orm.exc import NoResultFound


#VISTAS DE  LA BASE DE DATOS



class RegistroVista(Resource):
    def post(self):
        nombre_completo = request.json.get("nombre_completo")
        correo = request.json.get("correo")
        clave = request.json.get("clave")
        rol_usuario = request.json.get("rol_usuario")

        # Validar campos obligatorios
        if not nombre_completo or not correo or not clave:
            return {"mensaje": "Todos los campos son requeridos."}, 400

        # Verificar si el correo ya está en uso
        if Personal.query.filter_by(correo=correo).first():
            return {"mensaje": "El correo ya está registrado."}, 409

        nuevo_usuario = Personal(
            nombre_completo=nombre_completo,
            correo=correo,
            rol_usuario=rol_usuario
        )
        nuevo_usuario.clave = clave  # Aquí deberías implementar el hash de la contraseña
        db.session.add(nuevo_usuario)

        try:
            db.session.commit()
            return {"mensaje": "Usuario creado correctamente."}, 201
        except IntegrityError:
            db.session.rollback()
            return {"mensaje": "Error al crear el usuario."}, 500

class InicioSesiónVista(Resource):
    def post(self):
        correo = request.json.get("correo")
        clave = request.json.get("clave")

        personal = Personal.query.filter_by(correo=correo).first()

        if personal and personal.clave == clave:
            token = create_access_token(identity=personal.id)
            return {"token": token}, 200
        else:
            return {"mensaje": "Credenciales incorrectas."}, 401    


class PaginaPrincipalVista(Resource):
    def get(self):
        mensaje_bienvenida = "Bienvenido a nuestra tienda en línea. ¡Explora nuestros productos y disfruta de nuestras ofertas!"
        
        productos_destacados = Producto.query.filter(Producto.destacado == True).limit(5).all()
        productos_destacados_serializados = productos_schema.dump(productos_destacados)

        return {
            "mensaje": mensaje_bienvenida,
            "productos_destacados": productos_destacados_serializados
        }, 200





class ProductosVista(Resource):
    def obtener(self):
        productos = Producto.query.all()
        return productos_schema.dump(productos)

    def agregar(self):
        nombre_producto = request.json.get('nombre_producto')
        descripcion = request.json.get('descripcion')
        precio = request.json.get('precio')
        categoria_id = request.json.get('categoria_id')
        stock = request.json.get('stock')
        url_imagen = request.json.get('url_imagen')

        nuevo_producto = Producto(
            nombre_producto=nombre_producto,
            descripcion=descripcion,
            precio=precio,
            categoria_id=categoria_id,
            stock=stock,
            url_imagen=url_imagen
        )

        db.session.add(nuevo_producto)
        db.session.commit()
        return producto_schema.dump(nuevo_producto), 201

    

  
class CarritoVista(Resource):
    
    def obtener(self):
        identidad_usuario = get_jwt_identity()
        usuario = Personal.query.filter_by(correo=identidad_usuario).first()

        carrito = Carrito.query.filter_by(usuario_id=usuario.id).all()
        return carrito_schema.dump(carrito), 200

    
    def agregar(self):
        identidad_usuario = get_jwt_identity()
        usuario = Personal.query.filter_by(correo=identidad_usuario).first()

        id_producto = request.json.get('id_producto')
        cantidad = request.json.get('cantidad')

        producto = Producto.query.get(id_producto)
        if not producto:
            return {"mensaje": "Producto no encontrado."}, 404

        item_carrito = Carrito(
            usuario_id=usuario.id,
            producto_id=producto.id,
            cantidad=cantidad
        )

        db.session.add(item_carrito)
        db.session.commit()
        return carrito_schema.dump(item_carrito), 201


class PedidoVista(Resource):
  
    def obtener(self):
        identidad_usuario = get_jwt_identity()
        usuario = Personal.query.filter_by(correo=identidad_usuario).first()

        pedidos = Pedido.query.filter_by(usuario_id=usuario.id).all()
        return pedidos_schema.dump(pedidos), 200

   
    def crear(self):
        identidad_usuario = get_jwt_identity()
        usuario = Personal.query.filter_by(correo=identidad_usuario).first()

        carrito = Carrito.query.filter_by(usuario_id=usuario.id).all()
        if not carrito:
            return {"mensaje": "El carrito está vacío."}, 400

        nuevo_pedido = Pedido(usuario_id=usuario.id, estado="Pendiente")
        db.session.add(nuevo_pedido)
        db.session.commit()

        # Crear el detalle del pedido
        for item in carrito:
            detalle_pedido = DetallePedido(
                pedido_id=nuevo_pedido.id,
                producto_id=item.producto_id,
                cantidad=item.cantidad
            )
            db.session.add(detalle_pedido)

        db.session.commit()
        return {"mensaje": "Pedido realizado con éxito."}, 201


