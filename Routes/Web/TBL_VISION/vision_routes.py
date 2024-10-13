from flask import Blueprint, jsonify, request
from Database.Database import db, TBL_VISION, BITACORA_USUARIOS
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

vision_bp = Blueprint('vision_bp', __name__)

# Ruta para insertar una nueva visión
@vision_bp.route('/vision/insert', methods=['POST'])
def create_vision():
    data = request.get_json()
    vision_text = data.get('vision_text')

    if not vision_text:
        return jsonify({'error': 'El texto de la visión es obligatorio'}), 400

    new_vision = TBL_VISION(
        vision_text=vision_text
    )

    try:
        db.session.add(new_vision)
        db.session.commit()
        return jsonify({'message': 'Visión creada exitosamente'}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Ruta para visualizar todas las visiones
@vision_bp.route('/vision', methods=['GET'])
def get_all_visiones():
    visiones = TBL_VISION.query.all()
    result = [{
        'id_vision': vision.id_vision,
        'vision_text': vision.vision_text
    } for vision in visiones]
    return jsonify(result), 200

# Ruta para visualizar una visión por su ID
@vision_bp.route('/vision/<int:id>', methods=['GET'])
def get_vision(id):
    vision = TBL_VISION.query.get(id)
    if not vision:
        return jsonify({'error': 'Visión no encontrada'}), 404
    return jsonify({
        'id_vision': vision.id_vision,
        'vision_text': vision.vision_text
    }), 200

# Ruta para actualizar una visión por su ID
@vision_bp.route('/vision/update/<int:id>', methods=['PUT'])
def update_vision(id):
    data = request.get_json()
    vision = TBL_VISION.query.get(id)

    if not vision:
        return jsonify({'error': 'Visión no encontrada'}), 404

    vision_text = data.get('vision_text')
    if vision_text:
        vision.vision_text = vision_text

    try:
        db.session.commit()
        return jsonify({'message': 'Visión actualizada exitosamente'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Ruta para eliminar una visión por su ID
@vision_bp.route('/vision/delete/<int:id>', methods=['DELETE'])
def delete_vision(id):
    vision = TBL_VISION.query.get(id)
    if not vision:
        return jsonify({'error': 'Visión no encontrada'}), 404

    try:
        db.session.delete(vision)
        db.session.commit()
        return jsonify({'message': 'Visión eliminada exitosamente'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
