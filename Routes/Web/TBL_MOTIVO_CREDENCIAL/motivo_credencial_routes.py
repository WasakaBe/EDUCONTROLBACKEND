from flask import Blueprint, jsonify, request
from Database.Database import db, TBL_MOTIVO_CREDENCIAL
from sqlalchemy.exc import SQLAlchemyError

motivo_credencial_bp = Blueprint('motivo_credencial_bp', __name__)

# Ruta para obtener todos los motivos de credencial
@motivo_credencial_bp.route('/motivos_credencial', methods=['GET'])
def get_all_motivos_credencial():
    try:
        motivos_credencial = TBL_MOTIVO_CREDENCIAL.query.all()
        result = [{'id_motivo_credencial': motivo.id_motivo_credencial,
                   'nombre_motivo_credencial': motivo.nombre_motivo_credencial
                   } for motivo in motivos_credencial]
        return jsonify({'motivos_credencial': result})
    except Exception as e:
        print(f'Error al obtener los motivos de credencial: {str(e)}')
        return jsonify({'message': 'Error al obtener los motivos de credencial', 'error': str(e)}), 500

# Ruta para eliminar un motivo de credencial por su ID
@motivo_credencial_bp.route('/motivos_credencial/<int:id>', methods=['DELETE'])
def delete_motivo_credencial(id):
    motivo_credencial = TBL_MOTIVO_CREDENCIAL.query.get(id)
    if not motivo_credencial:
        return jsonify({'message': 'Motivo de credencial no encontrado'}), 404

    try:
        db.session.delete(motivo_credencial)
        db.session.commit()
        return jsonify({'message': 'Motivo de credencial eliminado exitosamente'})
    except Exception as e:
        print(f'Error al eliminar el motivo de credencial: {str(e)}')
        return jsonify({'message': 'Error al eliminar el motivo de credencial', 'error': str(e)}), 500

# Ruta para insertar un nuevo motivo de credencial
@motivo_credencial_bp.route('/motivos_credencial', methods=['POST'])
def insert_motivo_credencial():
    data = request.json
    if not data:
        return jsonify({'message': 'No se proporcionaron datos para insertar'}), 400

    try:
        nombre_motivo_credencial = data.get('nombre_motivo_credencial')
        if TBL_MOTIVO_CREDENCIAL.query.filter_by(nombre_motivo_credencial=nombre_motivo_credencial).first():
            return jsonify({'message': f'El motivo de credencial "{nombre_motivo_credencial}" ya está registrado. No se pueden repetir nombres de motivo de credencial.'}), 400

        nuevo_motivo_credencial = TBL_MOTIVO_CREDENCIAL(
            nombre_motivo_credencial=nombre_motivo_credencial
        )
        db.session.add(nuevo_motivo_credencial)
        db.session.commit()
        return jsonify({'message': 'Motivo de credencial insertado exitosamente'}), 201
    except Exception as e:
        print(f'Error al insertar el motivo de credencial: {str(e)}')
        return jsonify({'message': 'Error al insertar el motivo de credencial', 'error': str(e)}), 500

# Ruta para actualizar un motivo de credencial por su ID
@motivo_credencial_bp.route('/motivos_credencial/<int:id>', methods=['PUT'])
def update_motivo_credencial(id):
    data = request.json
    if not data:
        return jsonify({'message': 'No se proporcionaron datos para actualizar'}), 400

    motivo_credencial = TBL_MOTIVO_CREDENCIAL.query.get(id)
    if not motivo_credencial:
        return jsonify({'message': 'Motivo de credencial no encontrado'}), 404

    try:
        motivo_credencial.nombre_motivo_credencial = data.get('nombre_motivo_credencial', motivo_credencial.nombre_motivo_credencial)
        db.session.commit()
        return jsonify({'message': 'Motivo de credencial actualizado exitosamente'})
    except Exception as e:
        print(f'Error al actualizar el motivo de credencial: {str(e)}')
        return jsonify({'message': 'Error al actualizar el motivo de credencial', 'error': str(e)}), 500
