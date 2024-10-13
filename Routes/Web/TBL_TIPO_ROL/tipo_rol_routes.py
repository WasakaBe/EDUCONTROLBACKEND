from flask import Blueprint, jsonify, request
from Database.Database import db, TBL_TIPO_ROL  # Asegúrate de que las rutas de importación sean correctas
from sqlalchemy.exc import SQLAlchemyError

tipo_rol_bp = Blueprint('tipo_rol_bp', __name__)

# Ruta para insertar un nuevo tipo de rol
@tipo_rol_bp.route('/tipo_rol/insert', methods=['POST'])
def create_tipo_rol():
    data = request.get_json()
    nombre_tipo_rol = data.get('nombre_tipo_rol')

    if not nombre_tipo_rol:
        return jsonify({'error': 'El nombre del tipo de rol es obligatorio'}), 400

    new_tipo_rol = TBL_TIPO_ROL(nombre_tipo_rol=nombre_tipo_rol)

    try:
        db.session.add(new_tipo_rol)
        db.session.commit()
        return jsonify({'message': 'Tipo de rol creado exitosamente'}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Error al crear el tipo de rol: ' + str(e)}), 500

# Ruta para visualizar todos los tipos de rol
@tipo_rol_bp.route('/tipo_rol', methods=['GET'])
def get_all_tipo_rol():
    try:
        tipo_roles = TBL_TIPO_ROL.query.all()
        result = [{'id_tipo_rol': rol.id_tipo_rol, 'nombre_tipo_rol': rol.nombre_tipo_rol} for rol in tipo_roles]
        return jsonify(result), 200
    except SQLAlchemyError as e:
        return jsonify({'error': 'Error al obtener los tipos de rol: ' + str(e)}), 500

# Ruta para visualizar un tipo de rol por su ID
@tipo_rol_bp.route('/tipo_rol/<int:id>', methods=['GET'])
def get_tipo_rol(id):
    try:
        tipo_rol = TBL_TIPO_ROL.query.get(id)
        if not tipo_rol:
            return jsonify({'error': 'Tipo de rol no encontrado'}), 404
        return jsonify({'id_tipo_rol': tipo_rol.id_tipo_rol, 'nombre_tipo_rol': tipo_rol.nombre_tipo_rol}), 200
    except SQLAlchemyError as e:
        return jsonify({'error': 'Error al obtener el tipo de rol: ' + str(e)}), 500

# Ruta para actualizar un tipo de rol por su ID
@tipo_rol_bp.route('/tipo_rol/<int:id>', methods=['PUT'])
def update_tipo_rol(id):
    data = request.get_json()
    try:
        tipo_rol = TBL_TIPO_ROL.query.get(id)

        if not tipo_rol:
            return jsonify({'error': 'Tipo de rol no encontrado'}), 404

        nombre_tipo_rol = data.get('nombre_tipo_rol')
        if not nombre_tipo_rol:
            return jsonify({'error': 'El nombre del tipo de rol es obligatorio'}), 400

        tipo_rol.nombre_tipo_rol = nombre_tipo_rol

        db.session.commit()
        return jsonify({'message': 'Tipo de rol actualizado exitosamente'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Error al actualizar el tipo de rol: ' + str(e)}), 500

# Ruta para eliminar un tipo de rol por su ID
@tipo_rol_bp.route('/tipo_rol/<int:id>', methods=['DELETE'])
def delete_tipo_rol(id):
    try:
        tipo_rol = TBL_TIPO_ROL.query.get(id)
        if not tipo_rol:
            return jsonify({'error': 'Tipo de rol no encontrado'}), 404

        db.session.delete(tipo_rol)
        db.session.commit()
        return jsonify({'message': 'Tipo de rol eliminado exitosamente'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Error al eliminar el tipo de rol: ' + str(e)}), 500
