from flask import Blueprint, jsonify, request
from Database.Database import db, TBL_ACTIVIDADES_CULTURALES
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from base64 import b64encode, b64decode

actividades_culturales_bp = Blueprint('actividades_culturales_bp', __name__)

# Ruta para insertar una nueva actividad cultural
@actividades_culturales_bp.route('/actividades_culturales/insert', methods=['POST'])
def create_actividad_cultural():
    data = request.form
    nombre = data.get('nombre_actividad_cultural')
    descripcion = data.get('descripcion_actividad_cultural')
    imagen = request.files.get('imagen_actividad_cultural')

    if not all([nombre, descripcion, imagen]):
        return jsonify({'error': 'El nombre, la descripción y la imagen son obligatorios'}), 400

    try:
        new_actividad_cultural = TBL_ACTIVIDADES_CULTURALES(
            nombre_actividad_cultural=nombre,
            descripcion_actividad_cultural=descripcion,
            imagen_actividad_cultural=imagen.read()
        )
        db.session.add(new_actividad_cultural)
        db.session.commit()
        return jsonify({'message': 'Actividad cultural creada exitosamente'}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Ruta para visualizar todas las actividades culturales
@actividades_culturales_bp.route('/actividades_culturales', methods=['GET'])
def get_all_actividades_culturales():
    actividades_culturales = TBL_ACTIVIDADES_CULTURALES.query.all()
    result = [{
        'id_actividad_cultural': actividad.id_actividad_cultural,
        'nombre_actividad_cultural': actividad.nombre_actividad_cultural,
        'descripcion_actividad_cultural': actividad.descripcion_actividad_cultural,
        'imagen_actividad_cultural': b64encode(actividad.imagen_actividad_cultural).decode('utf-8') if actividad.imagen_actividad_cultural else None
    } for actividad in actividades_culturales]
    return jsonify(result), 200

# Ruta para visualizar una actividad cultural por su ID
@actividades_culturales_bp.route('/actividades_culturales/view/<int:id>', methods=['GET'])
def get_actividad_cultural(id):
    actividad_cultural = TBL_ACTIVIDADES_CULTURALES.query.get(id)
    if not actividad_cultural:
        return jsonify({'error': 'Actividad cultural no encontrada'}), 404
    return jsonify({
        'id_actividad_cultural': actividad_cultural.id_actividad_cultural,
        'nombre_actividad_cultural': actividad_cultural.nombre_actividad_cultural,
        'descripcion_actividad_cultural': actividad_cultural.descripcion_actividad_cultural,
        'imagen_actividad_cultural': b64encode(actividad_cultural.imagen_actividad_cultural).decode('utf-8') if actividad_cultural.imagen_actividad_cultural else None
    }), 200

# Ruta para actualizar una actividad cultural por su ID
@actividades_culturales_bp.route('/actividades_culturales/update/<int:id>', methods=['PUT'])
def update_actividad_cultural(id):
    data = request.form
    actividad_cultural = TBL_ACTIVIDADES_CULTURALES.query.get(id)

    if not actividad_cultural:
        return jsonify({'error': 'Actividad cultural no encontrada'}), 404

    actividad_cultural.nombre_actividad_cultural = data.get('nombre_actividad_cultural', actividad_cultural.nombre_actividad_cultural)
    actividad_cultural.descripcion_actividad_cultural = data.get('descripcion_actividad_cultural', actividad_cultural.descripcion_actividad_cultural)
    imagen = request.files.get('imagen_actividad_cultural')
    if imagen:
        actividad_cultural.imagen_actividad_cultural = imagen.read()

    try:
        db.session.commit()
        return jsonify({'message': 'Actividad cultural actualizada exitosamente'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Ruta para eliminar una actividad cultural por su ID
@actividades_culturales_bp.route('/actividades_culturales/delete/<int:id>', methods=['DELETE'])
def delete_actividad_cultural(id):
    actividad_cultural = TBL_ACTIVIDADES_CULTURALES.query.get(id)
    if not actividad_cultural:
        return jsonify({'error': 'Actividad cultural no encontrada'}), 404

    try:
        db.session.delete(actividad_cultural)
        db.session.commit()
        return jsonify({'message': 'Actividad cultural eliminada exitosamente'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500