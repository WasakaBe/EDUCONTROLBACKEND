from flask import Blueprint, jsonify, request
from Database.Database import db, TBL_TRASLADO
from sqlalchemy.exc import SQLAlchemyError

traslados_bp = Blueprint('traslados_bp', __name__)

# Ruta para insertar un nuevo traslado
@traslados_bp.route('/traslado/insert', methods=['POST'])
def create_traslado():
    data = request.get_json()
    nombre_traslado = data.get('nombre_traslado')
    
    if not nombre_traslado:
        return jsonify({'error': 'El nombre del traslado es obligatorio'}), 400

    new_traslado = TBL_TRASLADO(nombre_traslado=nombre_traslado)
    
    try:
        db.session.add(new_traslado)
        db.session.commit()
        return jsonify({'message': 'Traslado creado exitosamente'}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Ruta para visualizar todos los traslados
@traslados_bp.route('/traslado', methods=['GET'])
def get_all_traslados():
    traslados = TBL_TRASLADO.query.all()
    result = [{'id_traslado': traslado.id_traslado, 'nombre_traslado': traslado.nombre_traslado} for traslado in traslados]
    return jsonify(result), 200

# Ruta para visualizar un traslado por su ID
@traslados_bp.route('/traslado/<int:id>', methods=['GET'])
def get_traslado(id):
    traslado = TBL_TRASLADO.query.get(id)
    if not traslado:
        return jsonify({'error': 'Traslado no encontrado'}), 404
    return jsonify({'id_traslado': traslado.id_traslado, 'nombre_traslado': traslado.nombre_traslado}), 200

# Ruta para actualizar un traslado por su ID
@traslados_bp.route('/traslado/<int:id>', methods=['PUT'])
def update_traslado(id):
    data = request.get_json()
    traslado = TBL_TRASLADO.query.get(id)
    
    if not traslado:
        return jsonify({'error': 'Traslado no encontrado'}), 404

    nombre_traslado = data.get('nombre_traslado')
    if not nombre_traslado:
        return jsonify({'error': 'El nombre del traslado es obligatorio'}), 400

    traslado.nombre_traslado = nombre_traslado

    try:
        db.session.commit()
        return jsonify({'message': 'Traslado actualizado exitosamente'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Ruta para eliminar un traslado por su ID
@traslados_bp.route('/traslado/<int:id>', methods=['DELETE'])
def delete_traslado(id):
    traslado = TBL_TRASLADO.query.get(id)
    if not traslado:
        return jsonify({'error': 'Traslado no encontrado'}), 404

    try:
        db.session.delete(traslado)
        db.session.commit()
        return jsonify({'message': 'Traslado eliminado exitosamente'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
