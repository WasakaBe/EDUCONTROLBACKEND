from flask import Blueprint, jsonify, request
from Database.Database import db, TBL_SOBRE_NOSOTROS
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from base64 import b64encode, b64decode

sobre_nosotros_bp = Blueprint('sobre_nosotros_bp', __name__)

@sobre_nosotros_bp.route('/sobre_nosotros/insert', methods=['POST'])
def create_sobre_nosotros():
    try:
        data = request.form
        txt_info = data.get('txt_sobre_nosotros')
        imagen_info = request.files.get('imagen_sobre_nosotros')
        fecha_info = data.get('fecha_sobre_nosotros')

        # Log de verificación
        print(f'Texto: {txt_info}')
        print(f'Imagen: {imagen_info}')
        print(f'Fecha: {fecha_info}')

        if not all([txt_info, imagen_info]):
            return jsonify({'error': 'El texto y la imagen son obligatorios'}), 400

        # Leer y verificar la imagen
        imagen_leida = imagen_info.read()
        print(f'Imagen leída: {len(imagen_leida)} bytes')

        # Convertir la fecha si está presente, de lo contrario usar la fecha actual
        fecha_sobre_nosotros = datetime.strptime(fecha_info, '%Y-%m-%dT%H:%M') if fecha_info else datetime.now()

        new_sobre_nosotros = TBL_SOBRE_NOSOTROS(
            txt_sobre_nosotros=txt_info,
            imagen_sobre_nosotros=imagen_leida,
            fecha_sobre_nosotros=fecha_sobre_nosotros
        )

        db.session.add(new_sobre_nosotros)
        db.session.commit()
        return jsonify({'message': 'Información sobre nosotros creada exitosamente'}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f'Error SQLAlchemy: {str(e)}')
        return jsonify({'error': f'SQLAlchemyError: {str(e)}'}), 500
    except Exception as e:
        print(f'Error general: {str(e)}')
        return jsonify({'error': f'Exception: {str(e)}'}), 500

# Ruta para visualizar todas las informaciones sobre nosotros
@sobre_nosotros_bp.route('/sobre_nosotros', methods=['GET'])
def get_all_sobre_nosotros():
    try:
        sobre_nosotros = TBL_SOBRE_NOSOTROS.query.all()
        result = [{
            'id_sobre_nosotros': info.id_sobre_nosotros,
            'txt_sobre_nosotros': info.txt_sobre_nosotros,
            'imagen_sobre_nosotros': b64encode(info.imagen_sobre_nosotros).decode('utf-8') if info.imagen_sobre_nosotros else None,
            'fecha_sobre_nosotros': info.fecha_sobre_nosotros
        } for info in sobre_nosotros]
        return jsonify(result), 200
    except Exception as e:
        print(f'Error al obtener información: {str(e)}')
        return jsonify({'error': f'Exception: {str(e)}'}), 500

# Ruta para visualizar una información sobre nosotros por su ID
@sobre_nosotros_bp.route('/sobre_nosotros/<int:id>', methods=['GET'])
def get_sobre_nosotros(id):
    try:
        sobre_nosotros = TBL_SOBRE_NOSOTROS.query.get(id)
        if not sobre_nosotros:
            return jsonify({'error': 'Información sobre nosotros no encontrada'}), 404
        return jsonify({
            'id_sobre_nosotros': sobre_nosotros.id_sobre_nosotros,
            'txt_sobre_nosotros': sobre_nosotros.txt_sobre_nosotros,
            'imagen_sobre_nosotros': b64encode(sobre_nosotros.imagen_sobre_nosotros).decode('utf-8') if sobre_nosotros.imagen_sobre_nosotros else None,
            'fecha_sobre_nosotros': sobre_nosotros.fecha_sobre_nosotros
        }), 200
    except Exception as e:
        print(f'Error al obtener información por ID: {str(e)}')
        return jsonify({'error': f'Exception: {str(e)}'}), 500

# Ruta para actualizar una información sobre nosotros por su ID
@sobre_nosotros_bp.route('/sobre_nosotros/update/<int:id>', methods=['PUT'])
def update_sobre_nosotros(id):
    try:
        data = request.form
        sobre_nosotros = TBL_SOBRE_NOSOTROS.query.get(id)

        if not sobre_nosotros:
            return jsonify({'error': 'Información sobre nosotros no encontrada'}), 404

        sobre_nosotros.txt_sobre_nosotros = data.get('txt_sobre_nosotros', sobre_nosotros.txt_sobre_nosotros)
        imagen_info = request.files.get('imagen_sobre_nosotros')
        if imagen_info:
            sobre_nosotros.imagen_sobre_nosotros = imagen_info.read()
        sobre_nosotros.fecha_sobre_nosotros = datetime.strptime(data.get('fecha_sobre_nosotros'), '%Y-%m-%dT%H:%M') if data.get('fecha_sobre_nosotros') else sobre_nosotros.fecha_sobre_nosotros

        db.session.commit()
        return jsonify({'message': 'Información sobre nosotros actualizada exitosamente'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f'Error SQLAlchemy: {str(e)}')
        return jsonify({'error': f'SQLAlchemyError: {str(e)}'}), 500
    except Exception as e:
        print(f'Error general: {str(e)}')
        return jsonify({'error': f'Exception: {str(e)}'}), 500

# Ruta para eliminar una información sobre nosotros por su ID
@sobre_nosotros_bp.route('/sobre_nosotros/delete/<int:id>', methods=['DELETE'])
def delete_sobre_nosotros(id):
    try:
        sobre_nosotros = TBL_SOBRE_NOSOTROS.query.get(id)
        if not sobre_nosotros:
            return jsonify({'error': 'Información sobre nosotros no encontrada'}), 404

        db.session.delete(sobre_nosotros)
        db.session.commit()
        return jsonify({'message': 'Información sobre nosotros eliminada exitosamente'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f'Error SQLAlchemy: {str(e)}')
        return jsonify({'error': f'SQLAlchemyError: {str(e)}'}), 500
    except Exception as e:
        print(f'Error general: {str(e)}')
        return jsonify({'error': f'Exception: {str(e)}'}), 500
