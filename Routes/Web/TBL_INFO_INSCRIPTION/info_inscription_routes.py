from flask import Blueprint, jsonify, request
from Database.Database import db, TBL_INFO_INSCRIPTION
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from base64 import b64encode, b64decode

info_inscription_bp = Blueprint('info_inscription_bp', __name__)

# Ruta para insertar una nueva información de inscripción
@info_inscription_bp.route('/info_inscription/insert', methods=['POST'])
def create_info_inscription():
    data = request.form
    txt_info = data.get('txt_info_inscription')
    requeriments_info = data.get('requeriments_info_inscription')
    periodo_info = data.get('periodo_info_inscripcion')
    imagen_info = request.files.get('imagen_info_inscription')

    if not all([txt_info, requeriments_info, periodo_info, imagen_info]):
        return jsonify({'error': 'Todos los campos son obligatorios'}), 400

    new_info_inscription = TBL_INFO_INSCRIPTION(
        txt_info_inscription=txt_info,
        requeriments_info_inscription=requeriments_info,
        periodo_info_inscripcion=periodo_info,
        imagen_info_inscription=imagen_info.read()
    )

    try:
        db.session.add(new_info_inscription)
        db.session.commit()
        return jsonify({'message': 'Información de inscripción creada exitosamente'}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Ruta para visualizar todas las informaciones de inscripción
@info_inscription_bp.route('/info_inscription', methods=['GET'])
def get_all_info_inscription():
    info_inscriptions = TBL_INFO_INSCRIPTION.query.all()
    result = [{
        'id_info_inscription': info.id_info_inscription,
        'txt_info_inscription': info.txt_info_inscription,
        'requeriments_info_inscription': info.requeriments_info_inscription,
        'periodo_info_inscripcion': info.periodo_info_inscripcion,
        'imagen_info_inscription': b64encode(info.imagen_info_inscription).decode('utf-8') if info.imagen_info_inscription else None
    } for info in info_inscriptions]
    return jsonify(result), 200

# Ruta para visualizar una información de inscripción por su ID
@info_inscription_bp.route('/info_inscription/<int:id>', methods=['GET'])
def get_info_inscription(id):
    info_inscription = TBL_INFO_INSCRIPTION.query.get(id)
    if not info_inscription:
        return jsonify({'error': 'Información de inscripción no encontrada'}), 404
    return jsonify({
        'id_info_inscription': info_inscription.id_info_inscription,
        'txt_info_inscription': info_inscription.txt_info_inscription,
        'requeriments_info_inscription': info_inscription.requeriments_info_inscription,
        'periodo_info_inscripcion': info_inscription.periodo_info_inscripcion,
        'imagen_info_inscription': b64encode(info_inscription.imagen_info_inscription).decode('utf-8') if info_inscription.imagen_info_inscription else None
    }), 200

# Ruta para actualizar una información de inscripción por su ID
@info_inscription_bp.route('/info_inscription/update/<int:id>', methods=['PUT'])
def update_info_inscription(id):
    data = request.form
    info_inscription = TBL_INFO_INSCRIPTION.query.get(id)

    if not info_inscription:
        return jsonify({'error': 'Información de inscripción no encontrada'}), 404

    info_inscription.txt_info_inscription = data.get('txt_info_inscription', info_inscription.txt_info_inscription)
    info_inscription.requeriments_info_inscription = data.get('requeriments_info_inscription', info_inscription.requeriments_info_inscription)
    info_inscription.periodo_info_inscripcion = data.get('periodo_info_inscripcion', info_inscription.periodo_info_inscripcion)
    imagen_info = request.files.get('imagen_info_inscription')
    if imagen_info:
        info_inscription.imagen_info_inscription = imagen_info.read()

    try:
        db.session.commit()
        return jsonify({'message': 'Información de inscripción actualizada exitosamente'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Ruta para eliminar una información de inscripción por su ID
@info_inscription_bp.route('/info_inscription/delete/<int:id>', methods=['DELETE'])
def delete_info_inscription(id):
    info_inscription = TBL_INFO_INSCRIPTION.query.get(id)
    if not info_inscription:
        return jsonify({'error': 'Información de inscripción no encontrada'}), 404

    try:
        db.session.delete(info_inscription)
        db.session.commit()
        return jsonify({'message': 'Información de inscripción eliminada exitosamente'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
