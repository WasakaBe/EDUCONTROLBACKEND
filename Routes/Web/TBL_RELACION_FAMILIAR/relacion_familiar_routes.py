from flask import Blueprint, jsonify, request
from Database.Database import db, TBL_RELACION_FAMILIAR
from sqlalchemy.exc import SQLAlchemyError

relacion_familiar_bp = Blueprint('relacion_familiar_bp', __name__)

# Ruta para obtener todas las relaciones familiares
@relacion_familiar_bp.route('/relaciones_familiares', methods=['GET'])
def get_all_relaciones_familiares():
    try:
        relaciones_familiares = TBL_RELACION_FAMILIAR.query.all()
        result = [{'id_relacion_familiar': relacion.id_relacion_familiar,
                   'nombre_relacion_familiar': relacion.nombre_relacion_familiar
                   } for relacion in relaciones_familiares]
        return jsonify({'relaciones_familiares': result})
    except Exception as e:
        print(f'Error al obtener las relaciones familiares: {str(e)}')
        return jsonify({'message': 'Error al obtener las relaciones familiares', 'error': str(e)}), 500

# Ruta para eliminar una relación familiar por su ID
@relacion_familiar_bp.route('/relaciones_familiares/<int:id>', methods=['DELETE'])
def delete_relacion_familiar(id):
    relacion_familiar = TBL_RELACION_FAMILIAR.query.get(id)
    if not relacion_familiar:
        return jsonify({'message': 'Relación familiar no encontrada'}), 404

    try:
        db.session.delete(relacion_familiar)
        db.session.commit()
        return jsonify({'message': 'Relación familiar eliminada exitosamente'})
    except Exception as e:
        print(f'Error al eliminar la relación familiar: {str(e)}')
        return jsonify({'message': 'Error al eliminar la relación familiar', 'error': str(e)}), 500

# Ruta para insertar una nueva relación familiar
@relacion_familiar_bp.route('/relaciones_familiares', methods=['POST'])
def insert_relacion_familiar():
    data = request.json
    if not data:
        return jsonify({'message': 'No se proporcionaron datos para insertar'}), 400

    try:
        nombre_relacion_familiar = data.get('nombre_relacion_familiar')
        if TBL_RELACION_FAMILIAR.query.filter_by(nombre_relacion_familiar=nombre_relacion_familiar).first():
            return jsonify({'message': f'La relación familiar "{nombre_relacion_familiar}" ya está registrada. No se pueden repetir nombres de relación familiar.'}), 400

        nueva_relacion_familiar = TBL_RELACION_FAMILIAR(
            nombre_relacion_familiar=nombre_relacion_familiar
        )
        db.session.add(nueva_relacion_familiar)
        db.session.commit()
        return jsonify({'message': 'Relación familiar insertada exitosamente'}), 201
    except Exception as e:
        print(f'Error al insertar la relación familiar: {str(e)}')
        return jsonify({'message': 'Error al insertar la relación familiar', 'error': str(e)}), 500

# Ruta para actualizar una relación familiar por su ID
@relacion_familiar_bp.route('/relaciones_familiares/<int:id>', methods=['PUT'])
def update_relacion_familiar(id):
    data = request.json
    if not data:
        return jsonify({'message': 'No se proporcionaron datos para actualizar'}), 400

    relacion_familiar = TBL_RELACION_FAMILIAR.query.get(id)
    if not relacion_familiar:
        return jsonify({'message': 'Relación familiar no encontrada'}), 404

    try:
        relacion_familiar.nombre_relacion_familiar = data.get('nombre_relacion_familiar', relacion_familiar.nombre_relacion_familiar)
        db.session.commit()
        return jsonify({'message': 'Relación familiar actualizada exitosamente'})
    except Exception as e:
        print(f'Error al actualizar la relación familiar: {str(e)}')
        return jsonify({'message': 'Error al actualizar la relación familiar', 'error': str(e)}), 500
