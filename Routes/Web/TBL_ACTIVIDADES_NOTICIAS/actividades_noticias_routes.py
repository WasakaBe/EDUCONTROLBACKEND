from flask import Blueprint, jsonify, request
from Database.Database import db, TBL_ACTIVIDADES_NOTICIAS
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from base64 import b64encode

actividades_noticias_bp = Blueprint('actividades_noticias_bp', __name__)

# Ruta para insertar una nueva actividad/noticia
@actividades_noticias_bp.route('/actividades_noticias/insert', methods=['POST'])
def create_actividad_noticia():
    data = request.form
    titulo = data.get('titulo_actividad_noticia')
    descripcion = data.get('descripcion_actividad_noticia')
    imagen = request.files.get('imagen_actividad_noticia')
    fecha = data.get('fecha_actividad_noticias')

    if not all([titulo, descripcion, imagen, fecha]):
        return jsonify({'error': 'El título, la descripción, la imagen y la fecha son obligatorios'}), 400

    try:
        fecha_formateada = datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return jsonify({'error': 'Formato de fecha inválido'}), 400

    new_actividad_noticia = TBL_ACTIVIDADES_NOTICIAS(
        titulo_actividad_noticia=titulo,
        descripcion_actividad_noticia=descripcion,
        imagen_actividad_noticia=imagen.read(),
        fecha_actividad_noticias=fecha_formateada
    )

    try:
        db.session.add(new_actividad_noticia)
        db.session.commit()
        return jsonify({'message': 'Actividad/Noticia creada exitosamente'}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Ruta para visualizar todas las actividades/noticias
@actividades_noticias_bp.route('/actividades_noticias', methods=['GET'])
def get_all_actividades_noticias():
    try:
        actividades_noticias = TBL_ACTIVIDADES_NOTICIAS.query.all()
        result = [{
            'id_actividades_noticias': actividad.id_actividades_noticias,
            'titulo_actividad_noticia': actividad.titulo_actividad_noticia,
            'descripcion_actividad_noticia': actividad.descripcion_actividad_noticia,
            'imagen_actividad_noticia': b64encode(actividad.imagen_actividad_noticia).decode('utf-8') if actividad.imagen_actividad_noticia else None,
            'fecha_actividad_noticias': actividad.fecha_actividad_noticias
        } for actividad in actividades_noticias]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Ruta para visualizar una actividad/noticia por su ID
@actividades_noticias_bp.route('/actividades_noticias/<int:id>', methods=['GET'])
def get_actividad_noticia(id):
    try:
        actividad_noticia = TBL_ACTIVIDADES_NOTICIAS.query.get(id)
        if not actividad_noticia:
            return jsonify({'error': 'Actividad/Noticia no encontrada'}), 404
        return jsonify({
            'id_actividades_noticias': actividad_noticia.id_actividades_noticias,
            'titulo_actividad_noticia': actividad_noticia.titulo_actividad_noticia,
            'descripcion_actividad_noticia': actividad_noticia.descripcion_actividad_noticia,
            'imagen_actividad_noticia': b64encode(actividad_noticia.imagen_actividad_noticia).decode('utf-8') if actividad_noticia.imagen_actividad_noticia else None,
            'fecha_actividad_noticias': actividad_noticia.fecha_actividad_noticias
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Ruta para actualizar una actividad/noticia por su ID
@actividades_noticias_bp.route('/actividades_noticias/update/<int:id>', methods=['PUT'])
def update_actividad_noticia(id):
    try:
        data = request.form
        actividad_noticia = TBL_ACTIVIDADES_NOTICIAS.query.get(id)

        if not actividad_noticia:
            return jsonify({'error': 'Actividad/Noticia no encontrada'}), 404

        actividad_noticia.titulo_actividad_noticia = data.get('titulo_actividad_noticia', actividad_noticia.titulo_actividad_noticia)
        actividad_noticia.descripcion_actividad_noticia = data.get('descripcion_actividad_noticia', actividad_noticia.descripcion_actividad_noticia)
        imagen = request.files.get('imagen_actividad_noticia')
        if imagen:
            actividad_noticia.imagen_actividad_noticia = imagen.read()
        actividad_noticia.fecha_actividad_noticias = data.get('fecha_actividad_noticias', actividad_noticia.fecha_actividad_noticias)

        db.session.commit()
        return jsonify({'message': 'Actividad/Noticia actualizada exitosamente'}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Ruta para eliminar una actividad/noticia por su ID
@actividades_noticias_bp.route('/actividades_noticias/delete/<int:id>', methods=['DELETE'])
def delete_actividad_noticia(id):
    try:
        actividad_noticia = TBL_ACTIVIDADES_NOTICIAS.query.get(id)
        if not actividad_noticia:
            return jsonify({'error': 'Actividad/Noticia no encontrada'}), 404

        db.session.delete(actividad_noticia)
        db.session.commit()
        return jsonify({'message': 'Actividad/Noticia eliminada exitosamente'}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500
