from flask import Blueprint, jsonify, request
from Database.Database import TBL_DOCENTES, TBL_USUARIOS, db, TBL_NOTIFICACIONES_DOCENTES
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

notificaciones_docentes_bp = Blueprint('notificaciones_docentes_bp', __name__)

# Ruta para insertar una nueva notificación
@notificaciones_docentes_bp.route('/notificaciones_docentes/insert', methods=['POST'])
def create_notificacion_docente():
    data = request.form
    docente_id = data.get('docente_id')
    subject = data.get('subject_notificacion_doc')
    message = data.get('message_notificacion_doc')

    if not all([docente_id, subject, message]):
        return jsonify({'error': 'El ID del docente, asunto y mensaje son obligatorios'}), 400

    try:
        new_notificacion = TBL_NOTIFICACIONES_DOCENTES(
            docente_id=docente_id,
            subject_notificacion_doc=subject,
            message_notificacion_doc=message
        )

        db.session.add(new_notificacion)
        db.session.commit()
        return jsonify({'message': 'Notificación creada exitosamente'}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Ruta para visualizar todas las notificaciones
@notificaciones_docentes_bp.route('/notificaciones_docentes', methods=['GET'])
def get_all_notificaciones_docentes():
    try:
        notificaciones = TBL_NOTIFICACIONES_DOCENTES.query.all()
        result = [{
            'id_notificaciones_docentes': notificacion.id_notificaciones_docentes,
            'docente_id': notificacion.docente_id,
            'subject_notificacion_doc': notificacion.subject_notificacion_doc,
            'message_notificacion_doc': notificacion.message_notificacion_doc,
            'fecha_notificaciones_doc': notificacion.fecha_notificaciones_doc
        } for notificacion in notificaciones]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Ruta para visualizar una notificación por su ID
@notificaciones_docentes_bp.route('/notificaciones_docentes/<int:id>', methods=['GET'])
def get_notificacion_docente(id):
    try:
        notificacion = TBL_NOTIFICACIONES_DOCENTES.query.get(id)
        if not notificacion:
            return jsonify({'error': 'Notificación no encontrada'}), 404
        return jsonify({
            'id_notificaciones_docentes': notificacion.id_notificaciones_docentes,
            'docente_id': notificacion.docente_id,
            'subject_notificacion_doc': notificacion.subject_notificacion_doc,
            'message_notificacion_doc': notificacion.message_notificacion_doc,
            'fecha_notificaciones_doc': notificacion.fecha_notificaciones_doc
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Ruta para actualizar una notificación por su ID
@notificaciones_docentes_bp.route('/notificaciones_docentes/update/<int:id>', methods=['PUT'])
def update_notificacion_docente(id):
    try:
        data = request.form
        notificacion = TBL_NOTIFICACIONES_DOCENTES.query.get(id)

        if not notificacion:
            return jsonify({'error': 'Notificación no encontrada'}), 404

        notificacion.subject_notificacion_doc = data.get('subject_notificacion_doc', notificacion.subject_notificacion_doc)
        notificacion.message_notificacion_doc = data.get('message_notificacion_doc', notificacion.message_notificacion_doc)

        db.session.commit()
        return jsonify({'message': 'Notificación actualizada exitosamente'}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Ruta para eliminar una notificación por su ID
@notificaciones_docentes_bp.route('/notificaciones_docentes/delete/<int:id>', methods=['DELETE'])
def delete_notificacion_docente(id):
    try:
        notificacion = TBL_NOTIFICACIONES_DOCENTES.query.get(id)
        if not notificacion:
            return jsonify({'error': 'Notificación no encontrada'}), 404

        db.session.delete(notificacion)
        db.session.commit()
        return jsonify({'message': 'Notificación eliminada exitosamente'}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Ruta para obtener las notificaciones del docente asociado al usuario logueado
@notificaciones_docentes_bp.route('/notificaciones_docentes/user_docente/<int:user_id>', methods=['GET'])
def get_notificaciones_docente(user_id):
    try:
        # Paso 1: Verificar si el usuario existe en TBL_USUARIOS
        usuario = TBL_USUARIOS.query.filter_by(id_usuario=user_id).first()
        if not usuario:
            return jsonify({'error': 'Usuario no encontrado'}), 404

        # Paso 2: Obtener el id_docente asociado al usuario en TBL_DOCENTES
        docente = TBL_DOCENTES.query.filter_by(idUsuario=usuario.id_usuario).first()
        if not docente:
            return jsonify({'error': 'Docente asociado al usuario no encontrado'}), 404

        # Paso 3: Obtener las notificaciones del docente en TBL_NOTIFICACIONES_DOCENTES
        notificaciones = TBL_NOTIFICACIONES_DOCENTES.query.filter_by(docente_id=docente.id_docentes).all()

        if not notificaciones:
            return jsonify({'message': 'No hay notificaciones para este docente'}), 200

        # Formatear las notificaciones para la respuesta
        result = [{
            'id_notificaciones_docentes': notificacion.id_notificaciones_docentes,
            'docente_id': notificacion.docente_id,
            'subject_notificacion_doc': notificacion.subject_notificacion_doc,
            'message_notificacion_doc': notificacion.message_notificacion_doc,
            'fecha_notificaciones_doc': notificacion.fecha_notificaciones_doc
        } for notificacion in notificaciones]

        return jsonify(result), 200

    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500