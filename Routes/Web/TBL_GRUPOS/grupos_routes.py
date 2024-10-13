from flask import Blueprint, jsonify, request
from Database.Database import db, TBL_GRUPOS
from sqlalchemy.exc import SQLAlchemyError

grupos_bp = Blueprint('grupos_bp', __name__)

# Ruta para insertar un nuevo grupo
@grupos_bp.route('/grupo/insert', methods=['POST'])
def create_grupo():
    data = request.get_json()
    nombre_grupos = data.get('nombre_grupos')
    
    if not nombre_grupos:
        return jsonify({'error': 'El nombre del grupo es obligatorio'}), 400

    new_grupo = TBL_GRUPOS(nombre_grupos=nombre_grupos)
    
    try:
        db.session.add(new_grupo)
        db.session.commit()
        return jsonify({'message': 'Grupo creado exitosamente'}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e.orig)}), 500

# Ruta para visualizar todos los grupos
@grupos_bp.route('/grupo', methods=['GET'])
def get_all_grupos():
    try:
        grupos = TBL_GRUPOS.query.all()
        result = [{'id_grupos': grupo.id_grupos, 'nombre_grupos': grupo.nombre_grupos} for grupo in grupos]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'message': 'Error al obtener los grupos', 'error': str(e)}), 500


# Ruta para visualizar un grupo por su ID
@grupos_bp.route('/grupo/<int:id>', methods=['GET'])
def get_grupo(id):
    grupo = TBL_GRUPOS.query.get(id)
    if not grupo:
        return jsonify({'error': 'Grupo no encontrado'}), 404
    return jsonify({'id_grupos': grupo.id_grupos, 'nombre_grupos': grupo.nombre_grupos}), 200

# Ruta para actualizar un grupo por su ID
@grupos_bp.route('/grupo/<int:id>', methods=['PUT'])
def update_grupo(id):
    data = request.get_json()
    grupo = TBL_GRUPOS.query.get(id)
    
    if not grupo:
        return jsonify({'error': 'Grupo no encontrado'}), 404

    nombre_grupos = data.get('nombre_grupos')
    if not nombre_grupos:
        return jsonify({'error': 'El nombre del grupo es obligatorio'}), 400

    grupo.nombre_grupos = nombre_grupos

    try:
        db.session.commit()
        return jsonify({'message': 'Grupo actualizado exitosamente'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e.orig)}), 500

# Ruta para eliminar un grupo por su ID
@grupos_bp.route('/grupo/<int:id>', methods=['DELETE'])
def delete_grupo(id):
    grupo = TBL_GRUPOS.query.get(id)
    if not grupo:
        return jsonify({'error': 'Grupo no encontrado'}), 404

    try:
        db.session.delete(grupo)
        db.session.commit()
        return jsonify({'message': 'Grupo eliminado exitosamente'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e.orig)}), 500
