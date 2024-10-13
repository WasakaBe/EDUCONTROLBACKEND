from flask import Blueprint, jsonify, request
from Database.Database import TBL_ALUMNOS, TBL_DOCENTES, db, TBL_USUARIOS, BITACORA_SESION
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

register_bp = Blueprint('register_bp', __name__)

def send_email(to, subject, user_name):
    remitente = os.getenv('USER')
    destinatario = to
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = remitente
    msg['To'] = destinatario

    with open('Templates/email.html', 'r') as archivo:
        html_content = archivo.read()

    # Reemplaza la etiqueta {{user_name}} en el HTML con el nombre del usuario
    html_content = html_content.replace('{{user_name}}', user_name)

    msg.attach(MIMEText(html_content, 'html'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(remitente, os.getenv('PWD'))

    server.sendmail(remitente, destinatario, msg.as_string())
    server.quit()

@register_bp.route('/users/insert', methods=['POST'])
def insert_user():
    data = request.get_json()
    try:
        new_user = TBL_USUARIOS(
            nombre_usuario=data['nombre_usuario'],
            app_usuario=data['app_usuario'],
            apm_usuario=data.get('apm_usuario', ''),
            fecha_nacimiento_usuario=datetime.strptime(data['fecha_nacimiento_usuario'], '%Y-%m-%d'),
            token_usuario=data['token_usuario'],
            correo_usuario=data['correo_usuario'],
            pwd_usuario=data['pwd_usuario'],
            phone_usuario=data.get('phone_usuario'),
            idRol=data['idRol'],
            idSexo=data['idSexo'],
            ip_usuario=data['ip_usuario'],
            idCuentaActivo=data['idCuentaActivo'],
            idPregunta=data['idPregunta'],
            respuestaPregunta=data['respuestaPregunta'],
            foto_usuario=None
        )

        db.session.add(new_user)
        db.session.commit()

        send_email(data['correo_usuario'], 'Bienvenido a la aplicación', data['nombre_usuario'])

        new_sesion = BITACORA_SESION(
            id_usuario=new_user.id_usuario,
            nombre_usuario=new_user.nombre_usuario,
            correo_usuario=new_user.correo_usuario,
            fecha_inicio=datetime.now(),
            ip_usuario=request.remote_addr,
            url_solicitada=request.path
        )
        db.session.add(new_sesion)
        db.session.commit()

        return jsonify({'message': 'Usuario registrado exitosamente'}), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

#especial para enlazar alumnos con usuarios
@register_bp.route('/usuario/alumno/insert', methods=['POST'])
def insert_alumn_user():
    data = request.get_json()
    id_alumno = data.get('id_alumno', None)
    try:
        new_user = TBL_USUARIOS(
            nombre_usuario=data['nombre_usuario'],
            app_usuario=data['app_usuario'],
            apm_usuario=data.get('apm_usuario', ''),
            fecha_nacimiento_usuario=datetime.strptime(data['fecha_nacimiento_usuario'], '%Y-%m-%d'),
            token_usuario=data['token_usuario'],
            correo_usuario=data['correo_usuario'],
            pwd_usuario=data['pwd_usuario'],
            phone_usuario=data.get('phone_usuario'),
            idRol=data['idRol'],
            idSexo=data['idSexo'],
            ip_usuario=data['ip_usuario'],
            idCuentaActivo=data['idCuentaActivo'],
            idPregunta=data['idPregunta'],
            respuestaPregunta=data['respuestaPregunta'],
            foto_usuario=None
        )

        db.session.add(new_user)
        db.session.commit()

        # Asociar usuario con alumno si id_alumno es proporcionado
        if id_alumno:
            alumno = TBL_ALUMNOS.query.get(id_alumno)
            if alumno:
                alumno.idUsuario = new_user.id_usuario
                db.session.commit()

        send_email(data['correo_usuario'], 'Bienvenido a la aplicación', data['nombre_usuario'])

        new_sesion = BITACORA_SESION(
            id_usuario=new_user.id_usuario,
            nombre_usuario=new_user.nombre_usuario,
            correo_usuario=new_user.correo_usuario,
            fecha_inicio=datetime.now(),
            ip_usuario=request.remote_addr,
            url_solicitada=request.path
        )
        db.session.add(new_sesion)
        db.session.commit()

        return jsonify({'message': 'Usuario registrado exitosamente'}), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


#especial para enlazar docentes con usuarios
@register_bp.route('/usuario/docentes/insert', methods=['POST'])
def insert_docent_user():
    data = request.get_json()
    id_docente = data.get('id_docente', None)
    try:
        # Crear un nuevo usuario en TBL_USUARIOS
        new_user = TBL_USUARIOS(
            nombre_usuario=data['nombre_usuario'],
            app_usuario=data['app_usuario'],
            apm_usuario=data.get('apm_usuario', ''),
            fecha_nacimiento_usuario=datetime.strptime(data['fecha_nacimiento_usuario'], '%Y-%m-%d'),
            token_usuario=data['token_usuario'],
            correo_usuario=data['correo_usuario'],
            pwd_usuario=data['pwd_usuario'],
            phone_usuario=data.get('phone_usuario'),
            idRol=data['idRol'],
            idSexo=data['idSexo'],
            ip_usuario=data['ip_usuario'],
            idCuentaActivo=data['idCuentaActivo'],
            idPregunta=data['idPregunta'],
            respuestaPregunta=data['respuestaPregunta'],
            foto_usuario=None
        )

        db.session.add(new_user)
        db.session.commit()

        # Asociar usuario con docente si id_docente es proporcionado
        if id_docente:
            docente = TBL_DOCENTES.query.get(id_docente)
            if docente:
                docente.idUsuario = new_user.id_usuario
                db.session.commit()

        send_email(data['correo_usuario'], 'Bienvenido a la aplicación', data['nombre_usuario'])

        new_sesion = BITACORA_SESION(
            id_usuario=new_user.id_usuario,
            nombre_usuario=new_user.nombre_usuario,
            correo_usuario=new_user.correo_usuario,
            fecha_inicio=datetime.now(),
            ip_usuario=request.remote_addr,
            url_solicitada=request.path
        )
        db.session.add(new_sesion)
        db.session.commit()

        return jsonify({'message': 'Usuario registrado exitosamente'}), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
