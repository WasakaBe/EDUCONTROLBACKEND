from datetime import datetime
from flask import Blueprint, jsonify, request, current_app as app
from Database.Database import db, TBL_CREDENCIALES_ESCOLARES
from sqlalchemy.exc import SQLAlchemyError
from base64 import b64encode, b64decode

credenciales_escolares_bp = Blueprint('credenciales_escolares_bp', __name__)

# Ruta para insertar una nueva credencial escolar
@credenciales_escolares_bp.route('/credencial_escolar/insert', methods=['POST'])
def create_credencial_escolar():
    data = request.get_json()
    nombre_credencial_escolar = data.get('nombre_credencial_escolar')
    app_credencial_escolar = data.get('app_credencial_escolar')
    apm_credencial_escolar = data.get('apm_credencial_escolar')
    carrera_credencial_escolar = data.get('carrera_credencial_escolar')
    grupo_credencial_escolar = data.get('grupo_credencial_escolar')
    curp_credencial_escolar = data.get('curp_credencial_escolar')
    nocontrol_credencial_escolar = data.get('nocontrol_credencial_escolar')
    segsocial_credencial_escolar = data.get('segsocial_credencial_escolar')
    foto_credencial_escolar = data.get('foto_credencial_escolar')
    idalumnocrede = data.get('idalumnocrede')

    if not nombre_credencial_escolar or not app_credencial_escolar or not apm_credencial_escolar or not carrera_credencial_escolar or not grupo_credencial_escolar or not curp_credencial_escolar or not nocontrol_credencial_escolar or not segsocial_credencial_escolar or not idalumnocrede:
        return jsonify({'error': 'Todos los campos son obligatorios'}), 400

    new_credencial_escolar = TBL_CREDENCIALES_ESCOLARES(
        nombre_credencial_escolar=nombre_credencial_escolar,
        app_credencial_escolar=app_credencial_escolar,
        apm_credencial_escolar=apm_credencial_escolar,
        carrera_credencial_escolar=carrera_credencial_escolar,
        grupo_credencial_escolar=grupo_credencial_escolar,
        curp_credencial_escolar=curp_credencial_escolar,
        nocontrol_credencial_escolar=nocontrol_credencial_escolar,
        segsocial_credencial_escolar=segsocial_credencial_escolar,
        foto_credencial_escolar=b64decode(foto_credencial_escolar.encode('utf-8')) if foto_credencial_escolar else None,
        idalumnocrede=idalumnocrede
    )

    try:
        db.session.add(new_credencial_escolar)
        db.session.commit()
        return jsonify({'message': 'Credencial escolar creada exitosamente'}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Ruta para visualizar todas las credenciales escolares
@credenciales_escolares_bp.route('/credencial_escolar', methods=['GET'])
def get_all_credenciales_escolares():
    try:
        credenciales = TBL_CREDENCIALES_ESCOLARES.query.all()
        result = [{
            'id_credencial_escolar': credencial.id_credencial_escolar,
            'nombre_credencial_escolar': credencial.nombre_credencial_escolar,
            'app_credencial_escolar': credencial.app_credencial_escolar,
            'apm_credencial_escolar': credencial.apm_credencial_escolar,
            'carrera_credencial_escolar': credencial.carrera_credencial_escolar,
            'grupo_credencial_escolar': credencial.grupo_credencial_escolar,
            'curp_credencial_escolar': credencial.curp_credencial_escolar,
            'nocontrol_credencial_escolar': credencial.nocontrol_credencial_escolar,
            'segsocial_credencial_escolar': credencial.segsocial_credencial_escolar,
            'foto_credencial_escolar': b64encode(credencial.foto_credencial_escolar).decode('utf-8') if credencial.foto_credencial_escolar else None,
            'idalumnocrede': credencial.idalumnocrede
        } for credencial in credenciales]
        return jsonify(result), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        app.logger.error(f"Error fetching data from database: {str(e)}")
        return jsonify({'error': 'Error de la base de datos'}), 500

# Ruta para actualizar una credencial escolar
@credenciales_escolares_bp.route('/credencial_escolar/update/<int:id>', methods=['PUT'])
def update_credencial_escolar(id):
    data = request.get_json()
    try:
        credencial = TBL_CREDENCIALES_ESCOLARES.query.get(id)
        if not credencial:
            return jsonify({'error': 'Credencial escolar no encontrada'}), 404

        credencial.nombre_credencial_escolar = data.get('nombre_credencial_escolar')
        credencial.app_credencial_escolar = data.get('app_credencial_escolar')
        credencial.apm_credencial_escolar = data.get('apm_credencial_escolar')
        credencial.carrera_credencial_escolar = data.get('carrera_credencial_escolar')
        credencial.grupo_credencial_escolar = data.get('grupo_credencial_escolar')
        credencial.curp_credencial_escolar = data.get('curp_credencial_escolar')
        credencial.nocontrol_credencial_escolar = data.get('nocontrol_credencial_escolar')
        credencial.segsocial_credencial_escolar = data.get('segsocial_credencial_escolar')
        credencial.foto_credencial_escolar = b64decode(data.get('foto_credencial_escolar').encode('utf-8')) if data.get('foto_credencial_escolar') else None

        db.session.commit()
        return jsonify({'message': 'Credencial escolar actualizada exitosamente'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        app.logger.error(f"Error al actualizar la credencial escolar: {str(e)}")
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        app.logger.error(f"Unexpected error: {str(e)}")
        return jsonify({'error': str(e)}), 500


# Ruta para eliminar una credencial escolar
@credenciales_escolares_bp.route('/credencial_escolar/delete/<int:id>', methods=['DELETE'])
def delete_credencial_escolar(id):
    try:
        credencial = TBL_CREDENCIALES_ESCOLARES.query.get(id)
        if not credencial:
            return jsonify({'error': 'Credencial escolar no encontrada'}), 404

        db.session.delete(credencial)
        db.session.commit()
        return jsonify({'message': 'Credencial escolar eliminada exitosamente'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        app.logger.error(f"Error al eliminar la credencial escolar: {str(e)}")
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        app.logger.error(f"Unexpected error: {str(e)}")
        return jsonify({'error': str(e)}), 500