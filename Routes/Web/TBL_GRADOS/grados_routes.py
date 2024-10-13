from flask import Blueprint, jsonify, request
from Database.Database import db, TBL_GRADOS
from sqlalchemy.exc import SQLAlchemyError

grados_bp = Blueprint('grados_bp', __name__)

# Ruta para insertar un nuevo grado
@grados_bp.route('/grado/insert', methods=['POST'])
def create_grado():
    data = request.get_json()
    nombre_grado = data.get('nombre_grado')
    
    if not nombre_grado:
        return jsonify({'error': 'El nombre del grado es obligatorio'}), 400

    new_grado = TBL_GRADOS(nombre_grado=nombre_grado)
    
    try:
        db.session.add(new_grado)
        db.session.commit()
        return jsonify({'message': 'Grado creado exitosamente'}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Ruta para visualizar todos los grados
@grados_bp.route('/grado', methods=['GET'])
def get_all_grados():
    grados = TBL_GRADOS.query.all()
    result = [{'id_grado': grado.id_grado, 'nombre_grado': grado.nombre_grado} for grado in grados]
    return jsonify(result), 200

# Ruta para visualizar un grado por su ID
@grados_bp.route('/grado/<int:id>', methods=['GET'])
def get_grado(id):
    grado = TBL_GRADOS.query.get(id)
    if not grado:
        return jsonify({'error': 'Grado no encontrado'}), 404
    return jsonify({'id_grado': grado.id_grado, 'nombre_grado': grado.nombre_grado}), 200

# Ruta para actualizar un grado por su ID
@grados_bp.route('/grado/<int:id>', methods=['PUT'])
def update_grado(id):
    data = request.get_json()
    grado = TBL_GRADOS.query.get(id)
    
    if not grado:
        return jsonify({'error': 'Grado no encontrado'}), 404

    nombre_grado = data.get('nombre_grado')
    if not nombre_grado:
        return jsonify({'error': 'El nombre del grado es obligatorio'}), 400

    grado.nombre_grado = nombre_grado

    try:
        db.session.commit()
        return jsonify({'message': 'Grado actualizado exitosamente'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Ruta para eliminar un grado por su ID
@grados_bp.route('/grado/<int:id>', methods=['DELETE'])
def delete_grado(id):
    grado = TBL_GRADOS.query.get(id)
    if not grado:
        return jsonify({'error': 'Grado no encontrado'}), 404

    try:
        db.session.delete(grado)
        db.session.commit()
        return jsonify({'message': 'Grado eliminado exitosamente'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
