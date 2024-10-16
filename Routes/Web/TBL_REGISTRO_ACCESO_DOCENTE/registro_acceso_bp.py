from flask import Blueprint, jsonify, request
from Database.Database import TBL_DOCENTES, TBL_NOTIFICACIONES_DOCENTES, TBL_USUARIOS, TBL_REGISTRO_ACCESO_DOCENTE, db
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, time

registro_acceso_bp = Blueprint('registro_acceso_bp', __name__)

# Helper para determinar si es entrada o salida
def es_entrada(fecha_acceso):
    """Devuelve True si la hora es de entrada (6:00 a.m. - 11:59 a.m.), False si es de salida."""
    hora_actual = fecha_acceso.time()
    return time(6, 0) <= hora_actual <= time(11, 59)

@registro_acceso_bp.route('/docentes/acceso/<int:user_id>', methods=['POST'])
def registrar_acceso_docente(user_id):
    try:
        # 1. Obtener datos de la solicitud
        data = request.get_json()
        codigo_qr = data.get('codigoQr')

        if not codigo_qr:
            return jsonify({'error': 'Código QR no proporcionado'}), 400

        # 2. Verificar existencia del usuario y del docente
        usuario = TBL_USUARIOS.query.filter_by(id_usuario=user_id).first()
        if not usuario:
            return jsonify({'error': 'Usuario no encontrado'}), 404

        docente = TBL_DOCENTES.query.filter_by(idUsuario=usuario.id_usuario).first()
        if not docente:
            return jsonify({'error': 'Docente asociado al usuario no encontrado'}), 404

        # 3. Registrar el acceso del docente
        nombre_docente = f"{docente.nombre_docentes} {docente.app_docentes} {docente.apm_docentes}"
        fecha_acceso = datetime.now()  # Obtener la fecha y hora actuales

        nuevo_registro = TBL_REGISTRO_ACCESO_DOCENTE(
            id_docente=docente.id_docentes,
            nombre_docente=nombre_docente,
            fecha_registro_acceso=fecha_acceso,
            codigo_qr=codigo_qr
        )

        db.session.add(nuevo_registro)
        db.session.commit()

        # 4. Generar la notificación según la hora del acceso
        if es_entrada(fecha_acceso):
            subject = f"Notificación de Asistencia en el Acceso de entrada registrado para {nombre_docente}"
        else:
            subject = f"Notificación de Asistencia en el Acceso de salida registrado para {nombre_docente}"

        message = f"Accediste al plantel el {fecha_acceso.strftime('%Y-%m-%d %H:%M:%S')}."

        # 5. Registrar la notificación
        try:
            new_notificacion = TBL_NOTIFICACIONES_DOCENTES(
                docente_id=docente.id_docentes,
                subject_notificacion_doc=subject,
                message_notificacion_doc=message
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
            'nombre': nombre_docente,
            'fecha': fecha_acceso
        }), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': f"Error de base de datos: {str(e)}"}), 500
    except Exception as e:
        return jsonify({'error': f"Error inesperado: {str(e)}"}), 500
