from flask import Blueprint, jsonify, request
from Database.Database import db, TBL_MENSAJES_CONTACTOS
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

mensajes_contactos_bp = Blueprint('mensajes_contactos_bp', __name__)

@mensajes_contactos_bp.route('/mensaje_contacto/insert', methods=['POST'])
def create_mensaje_contacto():
    data = request.json
    if not data:
        return jsonify({'message': 'No se proporcionaron datos para insertar'}), 400

    nombre_mensaje_contacto = data.get('nombre_mensaje_contacto')
    correo_mensaje_contacto = data.get('correo_mensaje_contacto')
    motivo_mensaje_contacto = data.get('motivo_mensaje_contacto')
    fecha_mensaje = datetime.utcnow()

    if not nombre_mensaje_contacto or not correo_mensaje_contacto:
        return jsonify({'message': 'El nombre y el correo del mensaje de contacto son obligatorios'}), 400

    try:
        nuevo_mensaje_contacto = TBL_MENSAJES_CONTACTOS(
            nombre_mensaje_contacto=nombre_mensaje_contacto,
            correo_mensaje_contacto=correo_mensaje_contacto,
            motivo_mensaje_contacto=motivo_mensaje_contacto,
            fecha_mensaje=fecha_mensaje
        )
        db.session.add(nuevo_mensaje_contacto)
        db.session.commit()
        return jsonify({'message': 'Mensaje de contacto creado exitosamente'}), 201
    except SQLAlchemyError as e:
        print(f'Error al insertar el mensaje de contacto: {str(e)}')
        db.session.rollback()
        return jsonify({'message': 'Error al insertar el mensaje de contacto', 'error': str(e)}), 500

@mensajes_contactos_bp.route('/mensaje_contacto', methods=['GET'])
def get_all_mensajes_contacto():
    mensajes_contacto = TBL_MENSAJES_CONTACTOS.query.all()
    result = [{
        'id_mensaje_contacto': mensaje.id_mensaje_contacto,
        'nombre_mensaje_contacto': mensaje.nombre_mensaje_contacto,
        'correo_mensaje_contacto': mensaje.correo_mensaje_contacto,
        'motivo_mensaje_contacto': mensaje.motivo_mensaje_contacto,
        'fecha_mensaje': mensaje.fecha_mensaje
    } for mensaje in mensajes_contacto]
    return jsonify(result), 200

@mensajes_contactos_bp.route('/mensaje_contacto/<int:id>', methods=['GET'])
def get_mensaje_contacto(id):
    mensaje_contacto = TBL_MENSAJES_CONTACTOS.query.get(id)
    if not mensaje_contacto:
        return jsonify({'message': 'Mensaje de contacto no encontrado'}), 404
    return jsonify({
        'id_mensaje_contacto': mensaje_contacto.id_mensaje_contacto,
        'nombre_mensaje_contacto': mensaje_contacto.nombre_mensaje_contacto,
        'correo_mensaje_contacto': mensaje_contacto.correo_mensaje_contacto,
        'motivo_mensaje_contacto': mensaje_contacto.motivo_mensaje_contacto,
        'fecha_mensaje': mensaje_contacto.fecha_mensaje
    }), 200

@mensajes_contactos_bp.route('/mensaje_contacto/<int:id>', methods=['PUT'])
def update_mensaje_contacto(id):
    data = request.get_json()
    mensaje_contacto = TBL_MENSAJES_CONTACTOS.query.get(id)
    
    if not mensaje_contacto:
        return jsonify({'message': 'Mensaje de contacto no encontrado'}), 404

    nombre_mensaje_contacto = data.get('nombre_mensaje_contacto')
    correo_mensaje_contacto = data.get('correo_mensaje_contacto')
    motivo_mensaje_contacto = data.get('motivo_mensaje_contacto')
    fecha_mensaje = data.get('fecha_mensaje')

    if not nombre_mensaje_contacto or not correo_mensaje_contacto:
        return jsonify({'message': 'El nombre y el correo del mensaje de contacto son obligatorios'}), 400

    mensaje_contacto.nombre_mensaje_contacto = nombre_mensaje_contacto
    mensaje_contacto.correo_mensaje_contacto = correo_mensaje_contacto
    mensaje_contacto.motivo_mensaje_contacto = motivo_mensaje_contacto
    mensaje_contacto.fecha_mensaje = fecha_mensaje

    try:
        db.session.commit()
        return jsonify({'message': 'Mensaje de contacto actualizado exitosamente'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': 'Error al actualizar el mensaje de contacto', 'error': str(e)}), 500

@mensajes_contactos_bp.route('/mensaje_contacto/<int:id>', methods=['DELETE'])
def delete_mensaje_contacto(id):
    mensaje_contacto = TBL_MENSAJES_CONTACTOS.query.get(id)
    if not mensaje_contacto:
        return jsonify({'message': 'Mensaje de contacto no encontrado'}), 404

    try:
        db.session.delete(mensaje_contacto)
        db.session.commit()
        return jsonify({'message': 'Mensaje de contacto eliminado exitosamente'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': 'Error al eliminar el mensaje de contacto', 'error': str(e)}), 500
