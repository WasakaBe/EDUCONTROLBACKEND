from flask import Blueprint, jsonify, request
from Database.Database import db, TBL_ACTIVOS_CUENTAS
from sqlalchemy.exc import SQLAlchemyError

activos_cuentas_bp = Blueprint('activos_cuentas_bp', __name__)

# Ruta para insertar un nuevo activo de cuenta
@activos_cuentas_bp.route('/activo_cuenta/insert', methods=['POST'])
def create_activo_cuenta():
    data = request.get_json()
    nombre_activos_cuenta = data.get('nombre_activos_cuenta')
    
    if not nombre_activos_cuenta:
        return jsonify({'error': 'El nombre del activo de cuenta es obligatorio'}), 400

    new_activo_cuenta = TBL_ACTIVOS_CUENTAS(nombre_activos_cuenta=nombre_activos_cuenta)
    
    try:
        db.session.add(new_activo_cuenta)
        db.session.commit()
        return jsonify({'message': 'Activo de cuenta creado exitosamente'}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Ruta para visualizar todos los activos de cuenta
@activos_cuentas_bp.route('/activo_cuenta', methods=['GET'])
def get_all_activos_cuentas():
    activos_cuentas = TBL_ACTIVOS_CUENTAS.query.all()
    result = [{'id_activos_cuenta': activo.id_activos_cuenta, 'nombre_activos_cuenta': activo.nombre_activos_cuenta} for activo in activos_cuentas]
    return jsonify(result), 200

# Ruta para visualizar un activo de cuenta por su ID
@activos_cuentas_bp.route('/activo_cuenta/<int:id>', methods=['GET'])
def get_activo_cuenta(id):
    activo_cuenta = TBL_ACTIVOS_CUENTAS.query.get(id)
    if not activo_cuenta:
        return jsonify({'error': 'Activo de cuenta no encontrado'}), 404
    return jsonify({'id_activos_cuenta': activo_cuenta.id_activos_cuenta, 'nombre_activos_cuenta': activo_cuenta.nombre_activos_cuenta}), 200

# Ruta para actualizar un activo de cuenta por su ID
@activos_cuentas_bp.route('/activo_cuenta/<int:id>', methods=['PUT'])
def update_activo_cuenta(id):
    data = request.get_json()
    activo_cuenta = TBL_ACTIVOS_CUENTAS.query.get(id)
    
    if not activo_cuenta:
        return jsonify({'error': 'Activo de cuenta no encontrado'}), 404

    nombre_activos_cuenta = data.get('nombre_activos_cuenta')
    if not nombre_activos_cuenta:
        return jsonify({'error': 'El nombre del activo de cuenta es obligatorio'}), 400

    activo_cuenta.nombre_activos_cuenta = nombre_activos_cuenta

    try:
        db.session.commit()
        return jsonify({'message': 'Activo de cuenta actualizado exitosamente'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Ruta para eliminar un activo de cuenta por su ID
@activos_cuentas_bp.route('/activo_cuenta/<int:id>', methods=['DELETE'])
def delete_activo_cuenta(id):
    activo_cuenta = TBL_ACTIVOS_CUENTAS.query.get(id)
    if not activo_cuenta:
        return jsonify({'error': 'Activo de cuenta no encontrado'}), 404

    try:
        db.session.delete(activo_cuenta)
        db.session.commit()
        return jsonify({'message': 'Activo de cuenta eliminado exitosamente'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
