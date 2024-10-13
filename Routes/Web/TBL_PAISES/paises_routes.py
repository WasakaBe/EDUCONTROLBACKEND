from flask import Blueprint, jsonify, request
from Database.Database import db, TBL_PAISES
from base64 import b64encode, b64decode
from sqlalchemy.exc import SQLAlchemyError

paises_bp = Blueprint('paises_bp', __name__)

# Ruta para obtener todos los países
@paises_bp.route('/paises', methods=['GET'])
def get_all_paises():
    try:
        paises = TBL_PAISES.query.all()
        result = [{'id_pais': pais.id_pais,
                   'nombre_pais': pais.nombre_pais,
                   'foto_pais': b64encode(pais.foto_pais).decode('utf-8') if pais.foto_pais else None
                   } for pais in paises]
        return jsonify({'paises': result})
    except Exception as e:
        print(f'Error al obtener los países: {str(e)}')
        return jsonify({'message': 'Error al obtener los países', 'error': str(e)}), 500

# Ruta para eliminar un país por su ID
@paises_bp.route('/paises/<int:id>', methods=['DELETE'])
def delete_pais(id):
    pais = TBL_PAISES.query.get(id)
    if not pais:
        return jsonify({'message': 'País no encontrado'}), 404

    try:
        db.session.delete(pais)
        db.session.commit()
        return jsonify({'message': 'País eliminado exitosamente'})
    except Exception as e:
        print(f'Error al eliminar el país: {str(e)}')
        return jsonify({'message': 'Error al eliminar el país', 'error': str(e)}), 500

# Ruta para insertar un nuevo país
@paises_bp.route('/paises', methods=['POST'])
def insert_pais():
    data = request.json
    if not data:
        return jsonify({'message': 'No se proporcionaron datos para insertar'}), 400

    try:
        nombre_pais = data.get('nombre_pais')
        if TBL_PAISES.query.filter_by(nombre_pais=nombre_pais).first():
            return jsonify({'message': f'El país "{nombre_pais}" ya está registrado. No se pueden repetir nombres de país.'}), 400

        nuevo_pais = TBL_PAISES(
            nombre_pais=nombre_pais,
            foto_pais=b64decode(data.get('foto_pais').encode('utf-8')) if data.get('foto_pais') else None
        )
        db.session.add(nuevo_pais)
        db.session.commit()
        return jsonify({'message': 'País insertado exitosamente'}), 201
    except Exception as e:
        print(f'Error al insertar el país: {str(e)}')
        return jsonify({'message': 'Error al insertar el país', 'error': str(e)}), 500

# Ruta para actualizar un país por su ID
@paises_bp.route('/paises/<int:id>', methods=['PUT'])
def update_pais(id):
    data = request.json
    if not data:
        return jsonify({'message': 'No se proporcionaron datos para actualizar'}), 400

    pais = TBL_PAISES.query.get(id)
    if not pais:
        return jsonify({'message': 'País no encontrado'}), 404

    try:
        pais.nombre_pais = data.get('nombre_pais', pais.nombre_pais)
        if foto_pais := data.get('foto_pais'):
            pais.foto_pais = b64decode(foto_pais.encode('utf-8'))

        db.session.commit()
        return jsonify({'message': 'País actualizado exitosamente'})
    except Exception as e:
        print(f'Error al actualizar el país: {str(e)}')
        return jsonify({'message': 'Error al actualizar el país', 'error': str(e)}), 500
