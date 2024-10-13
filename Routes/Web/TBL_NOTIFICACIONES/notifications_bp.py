from flask import Blueprint, jsonify, request
from Database.Database import TBL_ALUMNOS, db, TBL_NOTIFICACIONES
from sqlalchemy.exc import SQLAlchemyError

notifications_bp = Blueprint('notifications_bp', __name__)

@notifications_bp.route('/notifications/delete', methods=['DELETE'])
def delete_notifications():
    data = request.get_json()
    notification_ids = data.get('ids')

    if not notification_ids:
        return jsonify({'error': 'No notification IDs provided'}), 400

    try:
        # Filtra las notificaciones que se deben eliminar
        notifications_to_delete = TBL_NOTIFICACIONES.query.filter(TBL_NOTIFICACIONES.id_notificaciones.in_(notification_ids)).all()
        
        if not notifications_to_delete:
            return jsonify({'error': 'No notifications found with the provided IDs'}), 404

        for notification in notifications_to_delete:
            db.session.delete(notification)
        
        db.session.commit()
        
        return jsonify({'message': 'Notificaciones eliminadas exitosamente'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Error de la base de datos: ' + str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'Error al eliminar las notificaciones: ' + str(e)}), 500


# Ruta para obtener las notificaciones de un alumno por su ID
@notifications_bp.route('/notificaciones/<int:alumno_id>', methods=['GET'])
def get_notificaciones(alumno_id):
    try:
        notificaciones = TBL_NOTIFICACIONES.query.filter_by(alumno_id=alumno_id).all()
        if not notificaciones:
            return jsonify({'message': 'No se encontraron notificaciones'}), 404

        result = [{
            'id_notificacion': notificacion.id_notificaciones,
            'subject_notificacion': notificacion.subject_notificacion,
            'message_notificacion': notificacion.message_notificacion,
            'fecha_notificaciones': notificacion.fecha_notificaciones
        } for notificacion in notificaciones]

        return jsonify(result), 200
    except SQLAlchemyError as e:
        return jsonify({'error': 'Error de la base de datos: ' + str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'Error al obtener las notificaciones: ' + str(e)}), 500
