from flask import Blueprint, jsonify, request
from Database.Database import db, TBL_USUARIOS, BITACORA_USUARIOS
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from random import randint

password_reset_bp = Blueprint('password_reset_bp', __name__)

def send_email(to, subject, content, template_path):
    remitente = os.getenv('USER')
    destinatario = to
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = remitente
    msg['To'] = destinatario

    with open(template_path, 'r') as archivo:
        html_content = archivo.read()

    html_content = html_content.replace('{{content}}', content)

    msg.attach(MIMEText(html_content, 'html'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(remitente, os.getenv('PWD'))

    server.sendmail(remitente, destinatario, msg.as_string())
    server.quit()

def log_action(user, action, details):
    bitacora_entry = BITACORA_USUARIOS(
        id_usuario=user.id_usuario,
        nombre_usuario=user.nombre_usuario,
        accion_realizada=action,
        detalles_accion=details,
        fecha_acceso=datetime.now(),
        ip_acceso=request.remote_addr
    )
    db.session.add(bitacora_entry)
    db.session.commit()

@password_reset_bp.route('/get-token', methods=['POST'])
def get_token():
    data = request.get_json()
    email = data.get('correo_usuario')
    if not email:
        return jsonify({'error': 'Email es requerido'}), 400

    user = TBL_USUARIOS.query.filter_by(correo_usuario=email).first()
    if user:
        token = ''.join([str(randint(0, 9)) for _ in range(6)])
        user.token_usuario = token
        try:
            db.session.commit()
            send_email(user.correo_usuario, 'Token de Recuperación', f'Su token de recuperación es: {token}', 'Templates/emailupdate.html')
            log_action(user, 'Solicitud de token', 'Token de recuperación enviado')
            return jsonify({'message': 'Token enviado a su correo electrónico'}), 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    return jsonify({'error': 'Usuario no encontrado'}), 404

@password_reset_bp.route('/verify-code', methods=['POST'])
def verify_code():
    data = request.get_json()
    token = data.get('token_usuario')
    if not token:
        return jsonify({'error': 'Token es requerido'}), 400

    user = TBL_USUARIOS.query.filter_by(token_usuario=token).first()
    if user:
        log_action(user, 'Verificación de token', 'Token verificado correctamente')
        return jsonify({'message': 'Token verificado'}), 200
    return jsonify({'error': 'Token incorrecto'}), 404

@password_reset_bp.route('/recover-password', methods=['POST'])
def recover_password():
    data = request.get_json()
    email = data.get('correo_usuario')
    id_pregunta = data.get('idPregunta')
    respuesta_pregunta = data.get('respuestaPregunta')

    if not email or not id_pregunta or not respuesta_pregunta:
        return jsonify({'error': 'Todos los campos son requeridos'}), 400

    user = TBL_USUARIOS.query.filter_by(correo_usuario=email, idPregunta=id_pregunta, respuestaPregunta=respuesta_pregunta).first()
    if user:
        log_action(user, 'Verificación de pregunta de seguridad', 'Pregunta y respuesta verificadas correctamente')
        return jsonify({'message': 'Pregunta y respuesta verificadas'}), 200
    return jsonify({'error': 'Las credenciales proporcionadas no coinciden'}), 404

@password_reset_bp.route('/updates-password', methods=['POST'])
def updates_password():
    data = request.get_json()
    email = data.get('correo_usuario')
    new_password = data.get('new_password')

    if not email or not new_password:
        return jsonify({'error': 'Todos los campos son requeridos'}), 400

    user = TBL_USUARIOS.query.filter_by(correo_usuario=email).first()
    if user:
        user.pwd_usuario = new_password
        try:
            db.session.commit()
            send_email(user.correo_usuario, 'Notificación de Actualización de Contraseña', 'Su contraseña ha sido restablecida correctamente', 'Templates/emailupdatepwd.html')
            log_action(user, 'Restablecimiento de contraseña', 'Contraseña restablecida correctamente')
            return jsonify({'message': 'Contraseña restablecida correctamente'}), 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    return jsonify({'error': 'Usuario no encontrado'}), 404
