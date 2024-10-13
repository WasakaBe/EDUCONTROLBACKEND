from flask import Blueprint, jsonify, request
from Database.Database import db, TBL_MISION, BITACORA_USUARIOS
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

mision_bp = Blueprint('mision_bp', __name__)

# Ruta para insertar una nueva misión
@mision_bp.route('/mision/insert', methods=['POST'])
def create_mision():
    data = request.get_json()
    mision_text = data.get('mision_text')

    if not mision_text:
        return jsonify({'error': 'El texto de la misión es obligatorio'}), 400

    new_mision = TBL_MISION(
        mision_text=mision_text
    )

    try:
        db.session.add(new_mision)
        db.session.commit()
        return jsonify({'message': 'Misión creada exitosamente'}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Ruta para visualizar todas las misiones
@mision_bp.route('/mision', methods=['GET'])
def get_all_misiones():
    misiones = TBL_MISION.query.all()
    result = [{
        'id_mision': mision.id_mision,
        'mision_text': mision.mision_text
    } for mision in misiones]
    return jsonify(result), 200

# Ruta para visualizar una misión por su ID
@mision_bp.route('/mision/<int:id>', methods=['GET'])
def get_mision(id):
    mision = TBL_MISION.query.get(id)
    if not mision:
        return jsonify({'error': 'Misión no encontrada'}), 404
    return jsonify({
        'id_mision': mision.id_mision,
        'mision_text': mision.mision_text
    }), 200

# Ruta para actualizar una misión por su ID
@mision_bp.route('/mision/update/<int:id>', methods=['PUT'])
def update_mision(id):
    data = request.get_json()
    mision = TBL_MISION.query.get(id)

    if not mision:
        return jsonify({'error': 'Misión no encontrada'}), 404

    mision_text = data.get('mision_text')
    if mision_text:
        mision.mision_text = mision_text

    try:
        db.session.commit()
        return jsonify({'message': 'Misión actualizada exitosamente'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Ruta para eliminar una misión por su ID
@mision_bp.route('/mision/delete/<int:id>', methods=['DELETE'])
def delete_mision(id):
    mision = TBL_MISION.query.get(id)
    if not mision:
        return jsonify({'error': 'Misión no encontrada'}), 404

    try:
        db.session.delete(mision)
        db.session.commit()
        return jsonify({'message': 'Misión eliminada exitosamente'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500