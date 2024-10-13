from flask import Blueprint, jsonify, request
from Database.Database import db, TBL_CARRERAS_TECNICAS
from base64 import b64encode, b64decode
from sqlalchemy.exc import SQLAlchemyError

carreras_tecnicas_bp = Blueprint('carreras_tecnicas_bp', __name__)

# Ruta para obtener todas las carreras técnicas
@carreras_tecnicas_bp.route('/carreras/tecnicas', methods=['GET'])
def get_all_carreras_tecnicas():
    try:
        carreras = TBL_CARRERAS_TECNICAS.query.all()
        result = [{'id_carrera_tecnica': carrera.id_carrera_tecnica,
                   'nombre_carrera_tecnica': carrera.nombre_carrera_tecnica,
                   'descripcion_carrera_tecnica': carrera.descripcion_carrera_tecnica,
                   'foto_carrera_tecnica': b64encode(carrera.foto_carrera_tecnica).decode('utf-8') if carrera.foto_carrera_tecnica else None
                   } for carrera in carreras]
        return jsonify({'carreras': result})
    except Exception as e:
        print(f'Error al obtener las carreras técnicas: {str(e)}')
        return jsonify({'message': 'Error al obtener las carreras técnicas', 'error': str(e)}), 500

# Ruta para eliminar una carrera técnica por su ID
@carreras_tecnicas_bp.route('/carreras/tecnicas/delete/<int:id>', methods=['DELETE'])
def delete_carrera_tecnica(id):
    carrera = TBL_CARRERAS_TECNICAS.query.get(id)
    if not carrera:
        return jsonify({'message': 'Carrera técnica no encontrada'}), 404

    try:
        db.session.delete(carrera)
        db.session.commit()
        return jsonify({'message': 'Carrera técnica eliminada exitosamente'})
    except Exception as e:
        print(f'Error al eliminar la carrera técnica: {str(e)}')
        return jsonify({'message': 'Error al eliminar la carrera técnica', 'error': str(e)}), 500

# Ruta para insertar una nueva carrera técnica
@carreras_tecnicas_bp.route('/carreras/tecnicas/insert', methods=['POST'])
def insert_carrera_tecnica():
    data = request.json
    if not data:
        return jsonify({'message': 'No se proporcionaron datos para insertar'}), 400

    try:
        nombre_carrera = data.get('nombre_carrera_tecnica')
        if TBL_CARRERAS_TECNICAS.query.filter_by(nombre_carrera_tecnica=nombre_carrera).first():
            return jsonify({'message': f'La carrera técnica "{nombre_carrera}" ya está registrada. No se pueden repetir nombres de carrera técnica.'}), 400

        nueva_carrera = TBL_CARRERAS_TECNICAS(
            nombre_carrera_tecnica=nombre_carrera,
            descripcion_carrera_tecnica=data.get('descripcion_carrera_tecnica'),
            foto_carrera_tecnica=b64decode(data.get('foto_carrera_tecnica').encode('utf-8')) if data.get('foto_carrera_tecnica') else None
        )
        db.session.add(nueva_carrera)
        db.session.commit()
        return jsonify({'message': 'Carrera técnica insertada exitosamente'}), 201
    except Exception as e:
        print(f'Error al insertar la carrera técnica: {str(e)}')
        return jsonify({'message': 'Error al insertar la carrera técnica', 'error': str(e)}), 500

# Ruta para actualizar una carrera técnica por su ID
@carreras_tecnicas_bp.route('/carreras/tecnicas/update/<int:id>', methods=['PUT'])
def update_carrera_tecnica(id):
    data = request.json
    if not data:
        return jsonify({'message': 'No se proporcionaron datos para actualizar'}), 400

    carrera = TBL_CARRERAS_TECNICAS.query.get(id)
    if not carrera:
        return jsonify({'message': 'Carrera técnica no encontrada'}), 404

    try:
        carrera.nombre_carrera_tecnica = data.get('nombre_carrera_tecnica', carrera.nombre_carrera_tecnica)
        carrera.descripcion_carrera_tecnica = data.get('descripcion_carrera_tecnica', carrera.descripcion_carrera_tecnica)

        if foto_carrera_tecnica := data.get('foto_carrera_tecnica'):
            carrera.foto_carrera_tecnica = b64decode(foto_carrera_tecnica.encode('utf-8'))

        db.session.commit()
        return jsonify({'message': 'Carrera técnica actualizada exitosamente'})
    except Exception as e:
        print(f'Error al actualizar la carrera técnica: {str(e)}')
        return jsonify({'message': 'Error al actualizar la carrera técnica', 'error': str(e)}), 500
