from flask import Blueprint, jsonify, request
from Database.Database import db, TBL_ASIGNATURAS
from sqlalchemy.exc import SQLAlchemyError

asignaturas_bp = Blueprint('asignaturas_bp', __name__)

# Ruta para insertar una nueva asignatura
@asignaturas_bp.route('/asignatura/insert', methods=['POST'])
def create_asignatura():
    data = request.get_json()
    nombre_asignatura = data.get('nombre_asignatura')
    
    if not nombre_asignatura:
        return jsonify({'error': 'El nombre de la asignatura es obligatorio'}), 400

    new_asignatura = TBL_ASIGNATURAS(nombre_asignatura=nombre_asignatura)
    
    try:
        db.session.add(new_asignatura)
        db.session.commit()
        return jsonify({'message': 'Asignatura creada exitosamente'}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e.orig)}), 500

# Ruta para visualizar todas las asignaturas
@asignaturas_bp.route('/asignatura', methods=['GET'])
def get_all_asignaturas():
    asignaturas = TBL_ASIGNATURAS.query.all()
    result = [{'id_asignatura': asignatura.id_asignatura, 'nombre_asignatura': asignatura.nombre_asignatura} for asignatura in asignaturas]
    return jsonify({'asignaturas': result}), 200

# Ruta para visualizar una asignatura por su ID
@asignaturas_bp.route('/asignatura/<int:id>', methods=['GET'])
def get_asignatura(id):
    asignatura = TBL_ASIGNATURAS.query.get(id)
    if not asignatura:
        return jsonify({'error': 'Asignatura no encontrada'}), 404
    return jsonify({'id_asignatura': asignatura.id_asignatura, 'nombre_asignatura': asignatura.nombre_asignatura}), 200

# Ruta para actualizar una asignatura por su ID
@asignaturas_bp.route('/asignatura/<int:id>', methods=['PUT'])
def update_asignatura(id):
    data = request.get_json()
    asignatura = TBL_ASIGNATURAS.query.get(id)
    
    if not asignatura:
        return jsonify({'error': 'Asignatura no encontrada'}), 404

    nombre_asignatura = data.get('nombre_asignatura')
    if not nombre_asignatura:
        return jsonify({'error': 'El nombre de la asignatura es obligatorio'}), 400

    asignatura.nombre_asignatura = nombre_asignatura

    try:
        db.session.commit()
        return jsonify({'message': 'Asignatura actualizada exitosamente'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e.orig)}), 500

# Ruta para eliminar una asignatura por su ID
@asignaturas_bp.route('/asignatura/<int:id>', methods=['DELETE'])
def delete_asignatura(id):
    asignatura = TBL_ASIGNATURAS.query.get(id)
    if not asignatura:
        return jsonify({'error': 'Asignatura no encontrada'}), 404

    try:
        db.session.delete(asignatura)
        db.session.commit()
        return jsonify({'message': 'Asignatura eliminada exitosamente'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e.orig)}), 500
