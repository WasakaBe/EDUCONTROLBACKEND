from flask import Blueprint, jsonify, request
from Database.Database import db, TBL_CLINICAS
from sqlalchemy.exc import SQLAlchemyError

clinicas_bp = Blueprint('clinicas_bp', __name__)

# Ruta para insertar una nueva clínica
@clinicas_bp.route('/clinica/insert', methods=['POST'])
def create_clinica():
    data = request.get_json()
    nombre_clinicas = data.get('nombre_clinicas')
    
    if not nombre_clinicas:
        return jsonify({'error': 'El nombre de la clínica es obligatorio'}), 400

    new_clinica = TBL_CLINICAS(nombre_clinicas=nombre_clinicas)
    
    try:
        db.session.add(new_clinica)
        db.session.commit()
        return jsonify({'message': 'Clínica creada exitosamente'}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Ruta para visualizar todas las clínicas
@clinicas_bp.route('/clinica', methods=['GET'])
def get_all_clinicas():
    clinicas = TBL_CLINICAS.query.all()
    result = [{'id_clinicas': clinica.id_clinicas, 'nombre_clinicas': clinica.nombre_clinicas} for clinica in clinicas]
    return jsonify(result), 200

# Ruta para visualizar una clínica por su ID
@clinicas_bp.route('/clinica/<int:id>', methods=['GET'])
def get_clinica(id):
    clinica = TBL_CLINICAS.query.get(id)
    if not clinica:
        return jsonify({'error': 'Clínica no encontrada'}), 404
    return jsonify({'id_clinicas': clinica.id_clinicas, 'nombre_clinicas': clinica.nombre_clinicas}), 200

# Ruta para actualizar una clínica por su ID
@clinicas_bp.route('/clinica/<int:id>', methods=['PUT'])
def update_clinica(id):
    data = request.get_json()
    clinica = TBL_CLINICAS.query.get(id)
    
    if not clinica:
        return jsonify({'error': 'Clínica no encontrada'}), 404

    nombre_clinicas = data.get('nombre_clinicas')
    if not nombre_clinicas:
        return jsonify({'error': 'El nombre de la clínica es obligatorio'}), 400

    clinica.nombre_clinicas = nombre_clinicas

    try:
        db.session.commit()
        return jsonify({'message': 'Clínica actualizada exitosamente'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Ruta para eliminar una clínica por su ID
@clinicas_bp.route('/clinica/<int:id>', methods=['DELETE'])
def delete_clinica(id):
    clinica = TBL_CLINICAS.query.get(id)
    if not clinica:
        return jsonify({'error': 'Clínica no encontrada'}), 404

    try:
        db.session.delete(clinica)
        db.session.commit()
        return jsonify({'message': 'Clínica eliminada exitosamente'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
