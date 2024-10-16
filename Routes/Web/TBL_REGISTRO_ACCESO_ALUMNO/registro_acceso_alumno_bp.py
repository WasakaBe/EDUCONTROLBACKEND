from flask import Blueprint, jsonify, request
from Database.Database import TBL_ALUMNOS, TBL_NOTIFICACIONES, TBL_REGISTRO_ACCESO_ALUMNO, TBL_USUARIOS, db
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, time

registro_acceso_alumnos_bp = Blueprint('registro_acceso_alumnos_bp', __name__)

# Helper para determinar si es entrada o salida
def es_entrada(fecha_acceso):
    """Devuelve True si la hora es de entrada (6:00 a.m. - 11:59 a.m.), False si es de salida."""
    hora_actual = fecha_acceso.time()
    return time(6, 0) <= hora_actual <= time(11, 59)

@registro_acceso_alumnos_bp.route('/alumnos/acceso/<int:alumno_id>', methods=['POST'])
def registrar_acceso_alumno(alumno_id):
    try:
        # 1. Obtener datos de la solicitud
        data = request.get_json()
        codigo_qr = data.get('codigoQr')

        if not codigo_qr:
            return jsonify({'error': 'Código QR no proporcionado'}), 400

        # 2. Verificar existencia del usuario y del alumno
        usuario = TBL_USUARIOS.query.filter_by(id_usuario=alumno_id).first()
        if not usuario:
            return jsonify({'error': 'Usuario no encontrado'}), 404

        alumno = TBL_ALUMNOS.query.filter_by(idUsuario=usuario.id_usuario).first()
        if not alumno:
            return jsonify({'error': 'Alumno no encontrado'}), 404

        # 3. Registrar el acceso del alumno
        nombre_alumno = f"{alumno.nombre_alumnos} {alumno.app_alumnos} {alumno.apm_alumnos}"
        fecha_acceso = datetime.now()  # Obtener la fecha y hora actuales

        nuevo_registro_alumno = TBL_REGISTRO_ACCESO_ALUMNO(
            id_alumnox=alumno.id_alumnos,
            nombre_alumnox=nombre_alumno,
            fecha_registro_acceso_alumno=fecha_acceso,
            codigo_qr_alumno=codigo_qr
        )

        db.session.add(nuevo_registro_alumno)
        db.session.commit()

        # 4. Generar la notificación de acuerdo a la hora del día
        if es_entrada(fecha_acceso):
            subject = f"Notificacion de Asistencia en el Acceso de entrada registrado para {nombre_alumno}"
        else:
            subject = f"Notificacion de Asistencia en el Acceso de salida registrado para {nombre_alumno}"

        message = f"Accediste al plantel el {fecha_acceso.strftime('%Y-%m-%d %H:%M:%S')}."

        # 5. Registrar la notificación
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
            return jsonify({
                'error': f"Registro de acceso exitoso, pero hubo un error al registrar la notificación: {str(e)}"
            }), 500

        # 6. Respuesta exitosa
        return jsonify({
            'message': 'Acceso registrado y notificación enviada exitosamente',
            'nombre': nombre_alumno,
            'fecha': fecha_acceso
        }), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': f"Error de base de datos: {str(e)}"}), 500
    except Exception as e:
        return jsonify({'error': f"Error inesperado: {str(e)}"}), 500
