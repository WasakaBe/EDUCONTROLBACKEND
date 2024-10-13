from flask import Blueprint, jsonify, request
from Database.Database import db, TBL_SEXOS
from sqlalchemy.exc import SQLAlchemyError

sexos_bp = Blueprint('sexos_bp', __name__)

# Ruta para insertar un nuevo sexo
@sexos_bp.route('/sexo/insert', methods=['POST'])
def create_sexo():
    data = request.get_json()
    nombre_sexo = data.get('nombre_sexo')
    
    if not nombre_sexo:
        return jsonify({'error': 'El nombre del sexo es obligatorio'}), 400

    new_sexo = TBL_SEXOS(nombre_sexo=nombre_sexo)
    
    try:
        db.session.add(new_sexo)
        db.session.commit()
        return jsonify({'message': 'Sexo creado exitosamente'}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Ruta para visualizar todos los sexos
@sexos_bp.route('/sexo', methods=['GET'])
def get_all_sexos():
    sexos = TBL_SEXOS.query.all()
    result = [{'id_sexos': sexo.id_sexos, 'nombre_sexo': sexo.nombre_sexo} for sexo in sexos]
    return jsonify(result), 200

# Ruta para visualizar un sexo por su ID
@sexos_bp.route('/sexo/<int:id>', methods=['GET'])
def get_sexo(id):
    sexo = TBL_SEXOS.query.get(id)
    if not sexo:
        return jsonify({'error': 'Sexo no encontrado'}), 404
    return jsonify({'id_sexos': sexo.id_sexos, 'nombre_sexo': sexo.nombre_sexo}), 200

# Ruta para actualizar un sexo por su ID
@sexos_bp.route('/sexo/<int:id>', methods=['PUT'])
def update_sexo(id):
    data = request.get_json()
    sexo = TBL_SEXOS.query.get(id)
    
    if not sexo:
        return jsonify({'error': 'Sexo no encontrado'}), 404

    nombre_sexo = data.get('nombre_sexo')
    if not nombre_sexo:
        return jsonify({'error': 'El nombre del sexo es obligatorio'}), 400

    sexo.nombre_sexo = nombre_sexo

    try:
        db.session.commit()
        return jsonify({'message': 'Sexo actualizado exitosamente'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Ruta para eliminar un sexo por su ID
@sexos_bp.route('/sexo/<int:id>', methods=['DELETE'])
def delete_sexo(id):
    sexo = TBL_SEXOS.query.get(id)
    if not sexo:
        return jsonify({'error': 'Sexo no encontrado'}), 404

    try:
        db.session.delete(sexo)
        db.session.commit()
        return jsonify({'message': 'Sexo eliminado exitosamente'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
