from flask import Blueprint, jsonify, request
from Database.Database import db, TBL_TRASLADO_TRANSPORTE
from sqlalchemy.exc import SQLAlchemyError

traslado_transporte_bp = Blueprint('traslado_transporte_bp', __name__)

# Ruta para insertar un nuevo traslado de transporte
@traslado_transporte_bp.route('/traslado_transporte/insert', methods=['POST'])
def create_traslado_transporte():
    data = request.get_json()
    nombre_traslado_transporte = data.get('nombre_traslado_transporte')
    
    if not nombre_traslado_transporte:
        return jsonify({'error': 'El nombre del traslado de transporte es obligatorio'}), 400

    new_traslado_transporte = TBL_TRASLADO_TRANSPORTE(nombre_traslado_transporte=nombre_traslado_transporte)
    
    try:
        db.session.add(new_traslado_transporte)
        db.session.commit()
        return jsonify({'message': 'Traslado de transporte creado exitosamente'}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Ruta para visualizar todos los traslados de transporte
@traslado_transporte_bp.route('/traslado_transporte', methods=['GET'])
def get_all_traslado_transporte():
    traslados_transporte = TBL_TRASLADO_TRANSPORTE.query.all()
    result = [{'id_traslado_transporte': traslado.id_traslado_transporte, 'nombre_traslado_transporte': traslado.nombre_traslado_transporte} for traslado in traslados_transporte]
    return jsonify(result), 200

# Ruta para visualizar un traslado de transporte por su ID
@traslado_transporte_bp.route('/traslado_transporte/<int:id>', methods=['GET'])
def get_traslado_transporte(id):
    traslado = TBL_TRASLADO_TRANSPORTE.query.get(id)
    if not traslado:
        return jsonify({'error': 'Traslado de transporte no encontrado'}), 404
    return jsonify({'id_traslado_transporte': traslado.id_traslado_transporte, 'nombre_traslado_transporte': traslado.nombre_traslado_transporte}), 200

# Ruta para actualizar un traslado de transporte por su ID
@traslado_transporte_bp.route('/traslado_transporte/<int:id>', methods=['PUT'])
def update_traslado_transporte(id):
    data = request.get_json()
    traslado = TBL_TRASLADO_TRANSPORTE.query.get(id)
    
    if not traslado:
        return jsonify({'error': 'Traslado de transporte no encontrado'}), 404

    nombre_traslado_transporte = data.get('nombre_traslado_transporte')
    if not nombre_traslado_transporte:
        return jsonify({'error': 'El nombre del traslado de transporte es obligatorio'}), 400

    traslado.nombre_traslado_transporte = nombre_traslado_transporte

    try:
        db.session.commit()
        return jsonify({'message': 'Traslado de transporte actualizado exitosamente'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Ruta para eliminar un traslado de transporte por su ID
@traslado_transporte_bp.route('/traslado_transporte/<int:id>', methods=['DELETE'])
def delete_traslado_transporte(id):
    traslado = TBL_TRASLADO_TRANSPORTE.query.get(id)
    if not traslado:
        return jsonify({'error': 'Traslado de transporte no encontrado'}), 404

    try:
        db.session.delete(traslado)
        db.session.commit()
        return jsonify({'message': 'Traslado de transporte eliminado exitosamente'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
