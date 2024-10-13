import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import smtplib
from Database.Database import BITACORA_SESION, db, TBL_USUARIOS
from flask import Blueprint, jsonify, request,current_app
import random
# Crear un blueprint para las ruta
wear_bp = Blueprint('wear_bp', __name__)

# Variable para almacenar el código generado
current_code = None

# Ruta para generar el código
@wear_bp.route('/generate-code', methods=['GET'])
def generate_code():
    global current_code
    current_code = str(random.randint(100000, 999999))
    return jsonify({'code': current_code})

# Ruta para verificar el código
@wear_bp.route('/verify-code', methods=['POST'])
def verify_code():
    data = request.json
    code = data.get('code')

    if code == current_code:
         # Obtener la información del usuario desde la base de datos
        tbl_user = TBL_USUARIOS.query.filter_by().first()
        # Crear el diccionario con la información del usuario
        user = {
                'id_usuario': tbl_user.id_usuario,
                'nombre_usuario': tbl_user.nombre_usuario,
                'app_usuario': tbl_user.app_usuario,
                'apm_usuario': tbl_user.apm_usuario,
                'fecha_nacimiento_usuario': tbl_user.fecha_nacimiento_usuario,
                'token_usuario': tbl_user.token_usuario,
                'correo_usuario': tbl_user.correo_usuario,
                'phone_usuario': tbl_user.phone_usuario,
                'idRol': tbl_user.idRol,
                'idSexo': tbl_user.idSexo,
                'idCuentaActivo': tbl_user.idCuentaActivo,
                'idPregunta': tbl_user.idPregunta,
                'respuestaPregunta': tbl_user.respuestaPregunta,
            }
        return jsonify({'message': 'Código correcto', 'user': user})
    else:
        return jsonify({'message': 'Código incorrecto'}), 400
    
