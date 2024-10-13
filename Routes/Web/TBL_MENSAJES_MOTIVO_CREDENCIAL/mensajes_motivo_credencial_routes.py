from datetime import datetime
from flask import Blueprint, jsonify, request
from Database.Database import TBL_ALUMNOS, TBL_MOTIVO_CREDENCIAL, TBL_USUARIOS, db, TBL_MENSAJES_MOTIVO_CREDENCIAL, BITACORA_USUARIOS
from sqlalchemy.exc import SQLAlchemyError

mensajes_motivo_credencial_bp = Blueprint('mensajes_motivo_credencial_bp', __name__)

# Ruta para insertar un nuevo mensaje motivo credencial
@mensajes_motivo_credencial_bp.route('/mensaje_motivo_credencial/insert', methods=['POST'])
def create_mensaje_motivo_credencial():
    data = request.get_json()
    idalumno = data.get('idalumno')
    idmotivo = data.get('idmotivo')
    fecha_motivo_credencial = data.get('fecha_motivo_credencial')

    if not idalumno or not idmotivo or not fecha_motivo_credencial:
        return jsonify({'error': 'Todos los campos son obligatorios'}), 400

    new_mensaje_motivo_credencial = TBL_MENSAJES_MOTIVO_CREDENCIAL(
        idalumno=idalumno,
        idmotivo=idmotivo,
        fecha_motivo_credencial=fecha_motivo_credencial
    )

    try:
        db.session.add(new_mensaje_motivo_credencial)
        db.session.commit()

        # Insertar un nuevo registro en BITACORA_USUARIOS
        user_ip = request.remote_addr
        new_bitacora = BITACORA_USUARIOS(
            id_usuario=idalumno,
            nombre_usuario="N/A",  # Asume que tienes un campo de nombre de usuario en la tabla de alumnos
            accion_realizada='Registro',
            detalles_accion='Mensaje motivo credencial registrado exitosamente',
            fecha_acceso=datetime.now(),
            ip_acceso=user_ip
        )
        db.session.add(new_bitacora)
        db.session.commit()

        return jsonify({'message': 'Mensaje motivo credencial creado exitosamente'}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@mensajes_motivo_credencial_bp.route('/mensaje_motivo_credencial', methods=['GET'])
def get_all_mensajes_motivo_credencial():
    try:
        mensajes = db.session.query(
            TBL_MENSAJES_MOTIVO_CREDENCIAL.id_mensajes_motivo_credencial,
            TBL_ALUMNOS.nombre_alumnos,
            TBL_ALUMNOS.app_alumnos,
            TBL_ALUMNOS.apm_alumnos,
            TBL_USUARIOS.correo_usuario,
            TBL_MOTIVO_CREDENCIAL.nombre_motivo_credencial,
            TBL_MENSAJES_MOTIVO_CREDENCIAL.fecha_motivo_credencial
        ).join(TBL_ALUMNOS, TBL_MENSAJES_MOTIVO_CREDENCIAL.idalumno == TBL_ALUMNOS.id_alumnos)\
         .join(TBL_USUARIOS, TBL_ALUMNOS.idUsuario == TBL_USUARIOS.id_usuario)\
         .join(TBL_MOTIVO_CREDENCIAL, TBL_MENSAJES_MOTIVO_CREDENCIAL.idmotivo == TBL_MOTIVO_CREDENCIAL.id_motivo_credencial).all()
        
        result = [{
            'id_mensajes_motivo_credencial': mensaje.id_mensajes_motivo_credencial,
            'nombre_alumnos': mensaje.nombre_alumnos,
            'app_alumnos': mensaje.app_alumnos,
            'apm_alumnos': mensaje.apm_alumnos,
            'correo_usuario': mensaje.correo_usuario,
            'nombre_motivo_credencial': mensaje.nombre_motivo_credencial,
            'fecha_motivo_credencial': mensaje.fecha_motivo_credencial
        } for mensaje in mensajes]
        
        return jsonify(result), 200
    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 500



@mensajes_motivo_credencial_bp.route('/mensaje_motivo_credencial/<int:id>', methods=['GET'])
def get_mensaje_motivo_credencial(id):
    mensaje = TBL_MENSAJES_MOTIVO_CREDENCIAL.query.get(id)
    if not mensaje:
        return jsonify({'error': 'Mensaje motivo credencial no encontrado'}), 404
    return jsonify({
        'id_mensajes_motivo_credencial': mensaje.id_mensajes_motivo_credencial,
        'id_alumno': mensaje.idalumno,
        'id_motivo': mensaje.idmotivo,
        'fecha_motivo_credencial': mensaje.fecha_motivo_credencial
    }), 200

@mensajes_motivo_credencial_bp.route('/mensaje_motivo_credencial/<int:id>', methods=['PUT'])
def update_mensaje_motivo_credencial(id):
    data = request.get_json()
    mensaje = TBL_MENSAJES_MOTIVO_CREDENCIAL.query.get(id)

    if not mensaje:
        return jsonify({'error': 'Mensaje motivo credencial no encontrado'}), 404

    id_alumno = data.get('id_alumno')
    id_motivo = data.get('id_motivo')
    fecha_motivo_credencial = data.get('fecha_motivo_credencial')

    if not id_alumno or not id_motivo or not fecha_motivo_credencial:
        return jsonify({'error': 'Todos los campos son obligatorios'}), 400

    mensaje.idalumno = id_alumno
    mensaje.idmotivo = id_motivo
    mensaje.fecha_motivo_credencial = fecha_motivo_credencial

    try:
        db.session.commit()

        # Insertar un nuevo registro en BITACORA_USUARIOS
        user_ip = request.remote_addr
        new_bitacora = BITACORA_USUARIOS(
            id_usuario=id_alumno,
            nombre_usuario="N/A",  # Asume que tienes un campo de nombre de usuario en la tabla de alumnos
            accion_realizada='Actualización',
            detalles_accion='Mensaje motivo credencial actualizado exitosamente',
            fecha_acceso=datetime.now(),
            ip_acceso=user_ip
        )
        db.session.add(new_bitacora)
        db.session.commit()

        return jsonify({'message': 'Mensaje motivo credencial actualizado exitosamente'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@mensajes_motivo_credencial_bp.route('/mensaje_motivo_credencial/<int:id>', methods=['DELETE'])
def delete_mensaje_motivo_credencial(id):
    mensaje = TBL_MENSAJES_MOTIVO_CREDENCIAL.query.get(id)
    if not mensaje:
        return jsonify({'error': 'Mensaje motivo credencial no encontrado'}), 404

    try:
        db.session.delete(mensaje)
        db.session.commit()

        # Insertar un nuevo registro en BITACORA_USUARIOS
        user_ip = request.remote_addr
        new_bitacora = BITACORA_USUARIOS(
            id_usuario=mensaje.idalumno,
            nombre_usuario="N/A",  # Asume que tienes un campo de nombre de usuario en la tabla de alumnos
            accion_realizada='Eliminación',
            detalles_accion='Mensaje motivo credencial eliminado exitosamente',
            fecha_acceso=datetime.now(),
            ip_acceso=user_ip
        )
        db.session.add(new_bitacora)
        db.session.commit()

        return jsonify({'message': 'Mensaje motivo credencial eliminado exitosamente'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
