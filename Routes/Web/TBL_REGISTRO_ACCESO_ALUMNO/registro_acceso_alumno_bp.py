from flask import Blueprint, jsonify, request
from Database.Database import TBL_ALUMNOS, TBL_NOTIFICACIONES, TBL_REGISTRO_ACCESO_ALUMNO, TBL_USUARIOS, db
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

registro_acceso_alumnos_bp = Blueprint('registro_acceso_alumnos_bp', __name__)


@registro_acceso_alumnos_bp.route('/alumnos/acceso/<int:alumno_id>', methods=['POST'])
def registrar_acceso_alumno(alumno_id):
    try:
        data = request.get_json()  # Obtiene los datos del cuerpo de la solicitud
        codigo_qr = data.get('codigoQr', None)

        if not codigo_qr:
            return jsonify({'error': 'Código QR no proporcionado'}), 400
                   # Verificar si el usuario existe en TBL_USUARIOS
        usuario = TBL_USUARIOS.query.filter_by(id_usuario=alumno_id).first()
        if not usuario:
            return jsonify({'error': 'Usuario no encontrado'}), 404

        # Verificar si el alumno existe en TBL_ALUMNOS
        alumno = TBL_ALUMNOS.query.filter_by(idUsuario=usuario.id_usuario).first()
        if not alumno:
            return jsonify({'error': 'Alumno no encontrado'}), 404

        # Registrar el acceso del alumno
        nombre_alumno = f"{alumno.nombre_alumnos} {alumno.app_alumnos} {alumno.apm_alumnos}"
        fecha_acceso = datetime.now()  # Registrar la fecha y hora actuales

        # Crear el registro de acceso para el alumno
        nuevo_registro_alumno = TBL_REGISTRO_ACCESO_ALUMNO(
            id_alumnox=alumno.id_alumnos,
            nombre_alumnox=nombre_alumno,
            fecha_registro_acceso_alumno=fecha_acceso,
            codigo_qr_alumno=codigo_qr  # Guardar el código QR si es necesario
        )

        db.session.add(nuevo_registro_alumno)
        db.session.commit()

        # Crear la notificación para el alumno
        subject = f"Notificacion de Asistencia en el Acceso registrado para {nombre_alumno}"
        message = f"Accediste al plantel el {fecha_acceso.strftime('%Y-%m-%d %H:%M:%S')}."

        try:
            new_notificacion = TBL_NOTIFICACIONES(
                alumno_id=alumno.id_alumnos,
                subject_notificacion=subject,
                message_notificacion=message
            )

            db.session.add(new_notificacion)
            db.session.commit()

        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({'error': f"Registro de acceso exitoso, pero hubo un error al registrar la notificación: {str(e)}"}), 500

        # Respuesta exitosa
        return jsonify({
            'message': 'Acceso registrado y notificación enviada exitosamente',
            'nombre': nombre_alumno,
            'fecha': fecha_acceso
        }), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500
