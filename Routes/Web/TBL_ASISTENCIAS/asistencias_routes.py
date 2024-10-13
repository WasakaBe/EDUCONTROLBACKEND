from flask import Blueprint, jsonify, request
from Database.Database import TBL_ALUMNOS, TBL_ASIGNATURAS, db, TBL_ASISTENCIAS
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

asistencias_bp = Blueprint('asistencias_bp', __name__)

# Ruta para registrar asistencia
@asistencias_bp.route('/asistencias/registrar', methods=['POST'])
def registrar_asistencia():
    data = request.get_json()
    
    id_alumno = data.get('id_alumno')
    id_horario = data.get('id_horario')
    fecha = data.get('fecha')
    estado_asistencia = data.get('estado_asistencia')
    comentarios = data.get('comentarios', '')

    if not all([id_alumno, id_horario, fecha, estado_asistencia]):
        return jsonify({'error': 'Todos los campos son obligatorios'}), 400

    try:
        nueva_asistencia = TBL_ASISTENCIAS(
            id_alumno=id_alumno,
            id_horario=id_horario,
            fecha=datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S'),
            estado_asistencia=estado_asistencia,
            comentarios=comentarios
        )

        db.session.add(nueva_asistencia)
        db.session.commit()

        return jsonify({'message': 'Asistencia registrada exitosamente'}), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Ruta para obtener todas las asistencias
@asistencias_bp.route('/asistencias', methods=['GET'])
def obtener_asistencias():
    try:
        asistencias = TBL_ASISTENCIAS.query.all()
        result = [{
            'id_asistencia': asistencia.id_asistencia,
            'id_alumno': asistencia.id_alumno,
            'id_horario': asistencia.id_horario,
            'fecha': asistencia.fecha.strftime('%Y-%m-%d %H:%M:%S'),
            'estado_asistencia': asistencia.estado_asistencia,
            'comentarios': asistencia.comentarios
        } for asistencia in asistencias]

        return jsonify(result), 200

    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 500

# Ruta para obtener las asistencias de un alumno específico
@asistencias_bp.route('/asistencias/alumno/<int:id_alumno>', methods=['GET'])
def obtener_asistencias_por_alumno(id_alumno):
    try:
        asistencias = TBL_ASISTENCIAS.query.filter_by(id_alumno=id_alumno).all()
        result = [{
            'id_asistencia': asistencia.id_asistencia,
            'id_alumno': asistencia.id_alumno,
            'id_horario': asistencia.id_horario,
            'fecha': asistencia.fecha.strftime('%Y-%m-%d %H:%M:%S'),
            'estado_asistencia': asistencia.estado_asistencia,
            'comentarios': asistencia.comentarios
        } for asistencia in asistencias]

        return jsonify(result), 200

    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 500

# Ruta para obtener las asistencias de un horario específico
@asistencias_bp.route('/asistencias/horario/<int:id_horario>', methods=['GET'])
def obtener_asistencias_por_horario(id_horario):
    try:
        asistencias = TBL_ASISTENCIAS.query.filter_by(id_horario=id_horario).all()
        result = [{
            'id_asistencia': asistencia.id_asistencia,
            'id_alumno': asistencia.id_alumno,
            'id_horario': asistencia.id_horario,
            'fecha': asistencia.fecha.strftime('%Y-%m-%d %H:%M:%S'),
            'estado_asistencia': asistencia.estado_asistencia,
            'comentarios': asistencia.comentarios
        } for asistencia in asistencias]

        return jsonify(result), 200

    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 500
