from flask import Blueprint, jsonify, request
from Database.Database import db, TBL_INFO_BECAS
from sqlalchemy.exc import SQLAlchemyError
from base64 import b64encode, b64decode

info_becas_bp = Blueprint('info_becas_bp', __name__)

# Ruta para insertar nueva información de beca
@info_becas_bp.route('/info_becas/insert', methods=['POST'])
def create_info_beca():
    data = request.form
    titulo = data.get('titulo_info_becas')
    descripcion = data.get('descripcion_info_becas')
    requisitos = data.get('requisitos_info_becas')
    imagen = request.files.get('foto_info_becas')

    if not all([titulo, descripcion, requisitos, imagen]):
        return jsonify({'error': 'El título, la descripción, los requisitos y la imagen son obligatorios'}), 400

    new_info_beca = TBL_INFO_BECAS(
        titulo_info_becas=titulo,
        descripcion_info_becas=descripcion,
        requisitos_info_becas=requisitos,
        foto_info_becas=imagen.read()
    )

    try:
        db.session.add(new_info_beca)
        db.session.commit()
        return jsonify({
            'id_info_becas': new_info_beca.id_info_becas,
            'titulo_info_becas': new_info_beca.titulo_info_becas,
            'descripcion_info_becas': new_info_beca.descripcion_info_becas,
            'requisitos_info_becas': new_info_beca.requisitos_info_becas,
            'foto_info_becas': b64encode(new_info_beca.foto_info_becas).decode('utf-8')
        }), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Ruta para obtener toda la información de becas
@info_becas_bp.route('/info_becas', methods=['GET'])
def get_all_info_becas():
    try:
        info_becas = TBL_INFO_BECAS.query.all()
        result = [{
            'id_info_becas': beca.id_info_becas,
            'titulo_info_becas': beca.titulo_info_becas,
            'descripcion_info_becas': beca.descripcion_info_becas,
            'requisitos_info_becas': beca.requisitos_info_becas,
            'foto_info_becas': b64encode(beca.foto_info_becas).decode('utf-8') if beca.foto_info_becas else None
        } for beca in info_becas]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Ruta para obtener una información de beca por ID
@info_becas_bp.route('/info_becas/<int:id>', methods=['GET'])
def get_info_beca(id):
    try:
        beca = TBL_INFO_BECAS.query.get(id)
        if not beca:
            return jsonify({'error': 'Información de beca no encontrada'}), 404
        return jsonify({
            'id_info_becas': beca.id_info_becas,
            'titulo_info_becas': beca.titulo_info_becas,
            'descripcion_info_becas': beca.descripcion_info_becas,
            'requisitos_info_becas': beca.requisitos_info_becas,
            'foto_info_becas': b64encode(beca.foto_info_becas).decode('utf-8') if beca.foto_info_becas else None
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Ruta para actualizar una información de beca por ID
@info_becas_bp.route('/info_becas/update/<int:id>', methods=['PUT'])
def update_info_beca(id):
    try:
        data = request.form
        beca = TBL_INFO_BECAS.query.get(id)

        if not beca:
            return jsonify({'error': 'Información de beca no encontrada'}), 404

        beca.titulo_info_becas = data.get('titulo_info_becas', beca.titulo_info_becas)
        beca.descripcion_info_becas = data.get('descripcion_info_becas', beca.descripcion_info_becas)
        beca.requisitos_info_becas = data.get('requisitos_info_becas', beca.requisitos_info_becas)
        imagen = request.files.get('foto_info_becas')
        if imagen:
            beca.foto_info_becas = imagen.read()

        db.session.commit()
        return jsonify({'message': 'Información de beca actualizada exitosamente'}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Ruta para eliminar una información de beca por ID
@info_becas_bp.route('/info_becas/delete/<int:id>', methods=['DELETE'])
def delete_info_beca(id):
    try:
        beca = TBL_INFO_BECAS.query.get(id)
        if not beca:
            return jsonify({'error': 'Información de beca no encontrada'}), 404

        db.session.delete(beca)
        db.session.commit()
        return jsonify({'message': 'Información de beca eliminada exitosamente'}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500
