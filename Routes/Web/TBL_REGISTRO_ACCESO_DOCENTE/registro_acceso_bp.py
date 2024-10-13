from flask import Blueprint, jsonify, request
from Database.Database import TBL_DOCENTES, TBL_NOTIFICACIONES_DOCENTES, TBL_USUARIOS, TBL_REGISTRO_ACCESO_DOCENTE, db
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

registro_acceso_bp = Blueprint('registro_acceso_bp', __name__)


@registro_acceso_bp.route('/docentes/acceso/<int:user_id>', methods=['POST'])
def registrar_acceso_docente(user_id):
    try:
        data = request.get_json()  # Obtiene los datos del cuerpo de la solicitud
        codigo_qr = data.get('codigoQr', None)

        if not codigo_qr:
            return jsonify({'error': 'Código QR no proporcionado'}), 400

        # Verificar si el usuario existe en TBL_USUARIOS
        usuario = TBL_USUARIOS.query.filter_by(id_usuario=user_id).first()
        if not usuario:
            return jsonify({'error': 'Usuario no encontrado'}), 404

        # Obtener el id_docente asociado al usuario en TBL_DOCENTES
        docente = TBL_DOCENTES.query.filter_by(idUsuario=usuario.id_usuario).first()
        if not docente:
            return jsonify({'error': 'Docente asociado al usuario no encontrado'}), 404

        # Registrar el acceso del docente
        nombre_docente = f"{docente.nombre_docentes} {docente.app_docentes} {docente.apm_docentes}"
        fecha_acceso = datetime.now()  # Registrar la fecha y hora actuales

        # Crear el registro de acceso
        nuevo_registro = TBL_REGISTRO_ACCESO_DOCENTE(
            id_docente=docente.id_docentes,
            nombre_docente=nombre_docente,
            fecha_registro_acceso=fecha_acceso,
            codigo_qr=codigo_qr  # Guardar el código QR si es necesario
        )

        db.session.add(nuevo_registro)
        db.session.commit()

        # Crear la notificación para el docente
        subject = f"Acceso registrado para {nombre_docente}"
        message = f"Accediste al plantel el {fecha_acceso.strftime('%Y-%m-%d %H:%M:%S')}."

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
            return jsonify({'error': f"Registro de acceso exitoso, pero hubo un error al registrar la notificación: {str(e)}"}), 500

        # Respuesta exitosa
        return jsonify({
            'message': 'Acceso registrado y notificación enviada exitosamente',
            'nombre': nombre_docente,
            'fecha': fecha_acceso
        }), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500
