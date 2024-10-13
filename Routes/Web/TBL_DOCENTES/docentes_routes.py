import os
from datetime import datetime
from flask import Blueprint, jsonify, request
from Database.Database import TBL_CLINICAS, TBL_SEXOS, TBL_USUARIOS, db, TBL_DOCENTES, BITACORA_USUARIOS
from sqlalchemy.exc import SQLAlchemyError
from base64 import b64encode, b64decode
import pandas as pd
from io import StringIO

docentes_bp = Blueprint('docentes_bp', __name__)

# Ruta para insertar un nuevo docente
@docentes_bp.route('/docente/insert', methods=['POST'])
def create_docente():
    data = request.get_json()
    nombre_docentes = data.get('nombre_docentes')
    app_docentes = data.get('app_docentes')
    apm_docentes = data.get('apm_docentes')
    fecha_nacimiento_docentes = data.get('fecha_nacimiento_docentes')
    noconttrol_docentes = data.get('noconttrol_docentes')
    telefono_docentes = data.get('telefono_docentes')
    foto_docentes = data.get('foto_docentes')
    seguro_social_docentes = data.get('seguro_social_docentes')
    idSexo = data.get('idSexo')
    idUsuario = data.get('idUsuario')
    idClinica = data.get('idClinica')

    if not all([nombre_docentes, app_docentes, apm_docentes, fecha_nacimiento_docentes, noconttrol_docentes, telefono_docentes, seguro_social_docentes]):
        return jsonify({'error': 'Los campos obligatorios no pueden estar vacíos'}), 400

    new_docente = TBL_DOCENTES(
        nombre_docentes=nombre_docentes,
        app_docentes=app_docentes,
        apm_docentes=apm_docentes,
        fecha_nacimiento_docentes=fecha_nacimiento_docentes,
        noconttrol_docentes=noconttrol_docentes,
        telefono_docentes=telefono_docentes,
        foto_docentes=b64decode(foto_docentes.encode('utf-8')) if foto_docentes else None,
        seguro_social_docentes=seguro_social_docentes,
        idSexo=idSexo,
        idUsuario=idUsuario,
        idClinica=idClinica
    )

    try:
        db.session.add(new_docente)
        db.session.commit()

        # Insertar un nuevo registro en BITACORA_USUARIOS
        user_ip = request.remote_addr
        new_bitacora = BITACORA_USUARIOS(
            id_usuario=idUsuario,
            nombre_usuario=new_docente.nombre_docentes,
            accion_realizada='Registro',
            detalles_accion='Docente registrado exitosamente',
            fecha_acceso=datetime.now(),
            ip_acceso=user_ip
        )
        db.session.add(new_bitacora)
        db.session.commit()

        return jsonify({'message': 'Docente creado exitosamente'}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Ruta para visualizar todos los docentes
@docentes_bp.route('/docente', methods=['GET'])
def get_all_docentes():
    try:
        docentes = TBL_DOCENTES.query.all()
        result = [{
            'id_docentes': docente.id_docentes,
            'nombre_docentes': docente.nombre_docentes,
            'app_docentes': docente.app_docentes,
            'apm_docentes': docente.apm_docentes,
            'fecha_nacimiento_docentes': docente.fecha_nacimiento_docentes.isoformat(),
            'noconttrol_docentes': docente.noconttrol_docentes,
            'telefono_docentes': docente.telefono_docentes,
            'foto_docentes': b64encode(docente.foto_docentes).decode('utf-8') if docente.foto_docentes else None,
            'seguro_social_docentes': docente.seguro_social_docentes,
            'idSexo': docente.idSexo,
            'idUsuario': docente.idUsuario,
            'idClinica': docente.idClinica
        } for docente in docentes]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'message': 'Error al obtener los docentes', 'error': str(e)}), 500



# Ruta para visualizar un docente por su ID
@docentes_bp.route('/docente/<int:id>', methods=['GET'])
def get_docente(id):
    docente = TBL_DOCENTES.query.get(id)
    if not docente:
        return jsonify({'error': 'Docente no encontrado'}), 404
    return jsonify({
        'id_docentes': docente.id_docentes,
        'nombre_docentes': docente.nombre_docentes,
        'app_docentes': docente.app_docentes,
        'apm_docentes': docente.apm_docentes,
        'fecha_nacimiento_docentes': docente.fecha_nacimiento_docentes.isoformat(),
        'noconttrol_docentes': docente.noconttrol_docentes,
        'telefono_docentes': docente.telefono_docentes,
        'foto_docentes': b64encode(docente.foto_docentes).decode('utf-8') if docente.foto_docentes else None,
        'seguro_social_docentes': docente.seguro_social_docentes,
        'idSexo': docente.idSexo,
        'idUsuario': docente.idUsuario,
        'idClinica': docente.idClinica
    }), 200

# Nueva ruta para visualizar un docente por su número de control o CURP
@docentes_bp.route('/docentes/nocontrol/<string:nocontrol>', methods=['GET'])
def get_docente_by_nocontrol(nocontrol):
    docente = TBL_DOCENTES.query.filter_by(noconttrol_docentes=nocontrol).first()
    if not docente:
        return jsonify({'error': 'Docente no encontrado'}), 404
    return jsonify({
        'id_docentes': docente.id_docentes,
        'nombre_docentes': docente.nombre_docentes,
        'app_docentes': docente.app_docentes,
        'apm_docentes': docente.apm_docentes,
        'fecha_nacimiento_docentes': docente.fecha_nacimiento_docentes.isoformat(),
        'noconttrol_docentes': docente.noconttrol_docentes,
        'telefono_docentes': docente.telefono_docentes,
        'foto_docentes': b64encode(docente.foto_docentes).decode('utf-8') if docente.foto_docentes else None,
        'seguro_social_docentes': docente.seguro_social_docentes,
        'idSexo': docente.idSexo,
        'idUsuario': docente.idUsuario,
        'idClinica': docente.idClinica
    }), 200

# Ruta para actualizar un docente por su ID
@docentes_bp.route('/docente/<int:id>', methods=['PUT'])
def update_docente(id):
    data = request.get_json()
    docente = TBL_DOCENTES.query.get(id)

    if not docente:
        return jsonify({'error': 'Docente no encontrado'}), 404

    nombre_docentes = data.get('nombre_docentes')
    app_docentes = data.get('app_docentes')
    apm_docentes = data.get('apm_docentes')
    fecha_nacimiento_docentes = data.get('fecha_nacimiento_docentes')
    noconttrol_docentes = data.get('noconttrol_docentes')
    telefono_docentes = data.get('telefono_docentes')
    foto_docentes = data.get('foto_docentes')
    seguro_social_docentes = data.get('seguro_social_docentes')
    idSexo = data.get('idSexo')
    idUsuario = data.get('idUsuario')
    idClinica = data.get('idClinica')

    if not all([nombre_docentes, app_docentes, apm_docentes, fecha_nacimiento_docentes, noconttrol_docentes, telefono_docentes, seguro_social_docentes]):
        return jsonify({'error': 'Los campos obligatorios no pueden estar vacíos'}), 400

    docente.nombre_docentes = nombre_docentes
    docente.app_docentes = app_docentes
    docente.apm_docentes = apm_docentes
    docente.fecha_nacimiento_docentes = fecha_nacimiento_docentes
    docente.noconttrol_docentes = noconttrol_docentes
    docente.telefono_docentes = telefono_docentes
    if foto_docentes:
        docente.foto_docentes = b64decode(foto_docentes.encode('utf-8'))
    docente.seguro_social_docentes = seguro_social_docentes
    docente.idSexo = idSexo
    docente.idUsuario = idUsuario
    docente.idClinica = idClinica

    try:
        db.session.commit()

        # Insertar un nuevo registro en BITACORA_USUARIOS
        user_ip = request.remote_addr
        new_bitacora = BITACORA_USUARIOS(
            id_usuario=idUsuario,
            nombre_usuario=docente.nombre_docentes,
            accion_realizada='Actualización',
            detalles_accion='Docente actualizado exitosamente',
            fecha_acceso=datetime.now(),
            ip_acceso=user_ip
        )
        db.session.add(new_bitacora)
        db.session.commit()

        return jsonify({'message': 'Docente actualizado exitosamente'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Ruta para eliminar un docente por su ID
@docentes_bp.route('/docente/<int:id>', methods=['DELETE'])
def delete_docente(id):
    docente = TBL_DOCENTES.query.get(id)
    if not docente:
        return jsonify({'error': 'Docente no encontrado'}), 404

    try:
        db.session.delete(docente)
        db.session.commit()

        # Insertar un nuevo registro en BITACORA_USUARIOS
        user_ip = request.remote_addr
        new_bitacora = BITACORA_USUARIOS(
            id_usuario=docente.idUsuario,
            nombre_usuario=docente.nombre_docentes,
            accion_realizada='Eliminación',
            detalles_accion='Docente eliminado exitosamente',
            fecha_acceso=datetime.now(),
            ip_acceso=user_ip
        )
        db.session.add(new_bitacora)
        db.session.commit()

        return jsonify({'message': 'Docente eliminado exitosamente'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@docentes_bp.route('/docente/usuario/<int:id_usuario>', methods=['GET'])
def get_docente_by_usuario(id_usuario):
    docente = db.session.query(
        TBL_DOCENTES, 
        TBL_SEXOS.nombre_sexo, 
        TBL_CLINICAS.nombre_clinicas, 
        TBL_USUARIOS.foto_usuario  # Añadir foto del usuario
    )\
    .join(TBL_SEXOS, TBL_DOCENTES.idSexo == TBL_SEXOS.id_sexos)\
    .join(TBL_CLINICAS, TBL_DOCENTES.idClinica == TBL_CLINICAS.id_clinicas)\
    .join(TBL_USUARIOS, TBL_DOCENTES.idUsuario == TBL_USUARIOS.id_usuario)\
    .filter(TBL_DOCENTES.idUsuario == id_usuario).first()
        
    if not docente:
        return jsonify({'error': 'Docente no encontrado'}), 404
    
    docente_data = docente[0]  # Datos del docente
    nombre_sexo = docente[1]  # Nombre del sexo
    nombre_clinica = docente[2]  # Nombre de la clínica
    foto_usuario = docente[3]  # Foto del usuario

    return jsonify({
        'id_docentes': docente_data.id_docentes,
        'nombre_docentes': docente_data.nombre_docentes,
        'app_docentes': docente_data.app_docentes,
        'apm_docentes': docente_data.apm_docentes,
        'foto_docentes': b64encode(foto_usuario).decode('utf-8') if foto_usuario else None,
        'fecha_nacimiento_docentes': docente_data.fecha_nacimiento_docentes,
        'noconttrol_docentes': docente_data.noconttrol_docentes,
        'telefono_docentes': docente_data.telefono_docentes,
        'seguro_social_docentes': docente_data.seguro_social_docentes,
        'sexo': nombre_sexo,  # Incluye el nombre del sexo en la respuesta
        'clinica': nombre_clinica,  # Incluye el nombre de la clínica en la respuesta
        'idUsuario': docente_data.idUsuario,
    }), 200


#subir alumnos por medio de un archivo CSV
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'csv'}
# Función para tratar con múltiples formatos de fecha
def parse_date(date_str):
    if pd.isnull(date_str):
        return None
    for fmt in ('%d/%m/%Y', '%Y-%m-%d', '%d-%m-%Y', '%Y/%m/%d'):
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return None


@docentes_bp.route('/docente/upload_csv', methods=['POST'])
def upload_docente_csv():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        try:
            df = pd.read_csv(file)

            required_columns = [
                'nombre_docentes', 'app_docentes', 'apm_docentes', 'fecha_nacimiento_docentes',
                'noconttrol_docentes', 'telefono_docentes', 'foto_docentes', 'seguro_social_docentes',
                'idSexo', 'idUsuario', 'idClinica'
            ]

            for column in required_columns:
                if column not in df.columns:
                    return jsonify({'error': f'Missing required column: {column}'}), 400

            df['fecha_nacimiento_docentes'] = df['fecha_nacimiento_docentes'].apply(lambda x: parse_date(str(x)) if pd.notnull(x) else None)

            if df['fecha_nacimiento_docentes'].isnull().any():
                return jsonify({'error': 'Invalid date format in fecha_nacimiento_docentes column'}), 400

            for _, row in df.iterrows():
                # Verificar si el registro ya existe
                existing_docente = TBL_DOCENTES.query.filter_by(noconttrol_docentes=row['noconttrol_docentes']).first()
                if existing_docente:
                    continue  # Saltar el registro si ya existe

                new_docente = TBL_DOCENTES(
                    nombre_docentes=row['nombre_docentes'],
                    app_docentes=row['app_docentes'],
                    apm_docentes=row['apm_docentes'],
                    fecha_nacimiento_docentes=row['fecha_nacimiento_docentes'],
                    noconttrol_docentes=row['noconttrol_docentes'],
                    telefono_docentes=row['telefono_docentes'],
                    foto_docentes=b64decode(row['foto_docentes'].encode('utf-8')) if pd.notnull(row['foto_docentes']) else None,
                    seguro_social_docentes=row['seguro_social_docentes'],
                    idSexo=row['idSexo'],
                    idUsuario=row['idUsuario'],
                    idClinica=row['idClinica'],
                )
                db.session.add(new_docente)
            db.session.commit()

            return jsonify({'message': 'Archivo CSV subido exitosamente'}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    return jsonify({'error': 'Invalid file'}), 400
