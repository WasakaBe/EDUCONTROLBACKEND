from datetime import datetime
from flask import Blueprint, jsonify, request
from Database.Database import db, TBL_SOLICITANTES, TBL_RELACION_FAMILIAR, TBL_CARRERAS_TECNICAS, TBL_INFO_BECAS
from sqlalchemy.exc import SQLAlchemyError
from base64 import b64encode

solicitantes_bp = Blueprint('solicitantes_bp', __name__)

# Ruta para insertar un nuevo solicitante
@solicitantes_bp.route('/solicitantes/insert', methods=['POST'])
def create_solicitante():
    data = request.form
    ficha_no = data.get('ficha_no')
    apellido_paterno = data.get('apellido_paterno')
    apellido_materno = data.get('apellido_materno')
    nombres = data.get('nombres')
    direccion = data.get('direccion')
    localidad = data.get('localidad')
    municipio = data.get('municipio')
    edad = data.get('edad')
    promedio_sec = data.get('promedio_sec')
    fecha_nacimiento = data.get('fecha_nacimiento')
    beca = data.get('beca')
    tipo_discapacidad = data.get('tipo_discapacidad')
    hablante_lengua_indigena = data.get('hablante_lengua_indigena')
    correo_electronico = data.get('correo_electronico')
    escuela_procedencia = data.get('escuela_procedencia')
    cct = data.get('cct')
    tipo_secundaria = data.get('tipo_secundaria')
    direccion_secundaria = data.get('direccion_secundaria')
    localidad_secundaria = data.get('localidad_secundaria')
    municipio_secundaria = data.get('municipio_secundaria')
    estado_secundaria = data.get('estado_secundaria')
    nombre_padre_tutor = data.get('nombre_padre_tutor')
    id_relacion_familiar = data.get('id_relacion_familiar')
    telefono_alumno = data.get('telefono_alumno')
    telefono_tutor = data.get('telefono_tutor')
    telefono_familiar = data.get('telefono_familiar')
    id_carrera_tecnica = data.get('id_carrera_tecnica')
    id_info_becas = data.get('id_info_becas')
    foto = request.files.get('foto')

    if not ficha_no or not apellido_paterno or not nombres or not direccion or not correo_electronico:
        return jsonify({'error': 'Los campos obligatorios no pueden estar vacíos'}), 400

    new_solicitante = TBL_SOLICITANTES(
        ficha_no=ficha_no,
        apellido_paterno=apellido_paterno,
        apellido_materno=apellido_materno,
        nombres=nombres,
        foto=foto.read() if foto else None,
        direccion=direccion,
        localidad=localidad,
        municipio=municipio,
        edad=int(edad),
        promedio_sec=float(promedio_sec),
        fecha_nacimiento=datetime.strptime(fecha_nacimiento, '%Y-%m-%d'),
        beca=bool(beca),
        tipo_discapacidad=tipo_discapacidad,
        hablante_lengua_indigena=bool(hablante_lengua_indigena),
        correo_electronico=correo_electronico,
        escuela_procedencia=escuela_procedencia,
        cct=cct,
        tipo_secundaria=tipo_secundaria,
        direccion_secundaria=direccion_secundaria,
        localidad_secundaria=localidad_secundaria,
        municipio_secundaria=municipio_secundaria,
        estado_secundaria=estado_secundaria,
        nombre_padre_tutor=nombre_padre_tutor,
        id_relacion_familiar=id_relacion_familiar,
        telefono_alumno=telefono_alumno,
        telefono_tutor=telefono_tutor,
        telefono_familiar=telefono_familiar,
        id_carrera_tecnica=id_carrera_tecnica,
        id_info_becas=id_info_becas
    )

    try:
        db.session.add(new_solicitante)
        db.session.commit()
        return jsonify({'message': 'Solicitante creado exitosamente'}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Ruta para visualizar todos los solicitantes
@solicitantes_bp.route('/solicitantes', methods=['GET'])
def get_all_solicitantes():
    solicitantes = TBL_SOLICITANTES.query.all()
    result = [{
        'id_solicitante': solicitante.id_solicitante,
        'ficha_no': solicitante.ficha_no,
        'apellido_paterno': solicitante.apellido_paterno,
        'apellido_materno': solicitante.apellido_materno,
        'nombres': solicitante.nombres,
        'foto': b64encode(solicitante.foto).decode('utf-8') if solicitante.foto else None,
        'direccion': solicitante.direccion,
        'localidad': solicitante.localidad,
        'municipio': solicitante.municipio,
        'edad': solicitante.edad,
        'promedio_sec': solicitante.promedio_sec,
        'fecha_nacimiento': solicitante.fecha_nacimiento.strftime('%Y-%m-%d'),
        'beca': solicitante.beca,
        'tipo_discapacidad': solicitante.tipo_discapacidad,
        'hablante_lengua_indigena': solicitante.hablante_lengua_indigena,
        'correo_electronico': solicitante.correo_electronico,
        'escuela_procedencia': solicitante.escuela_procedencia,
        'cct': solicitante.cct,
        'tipo_secundaria': solicitante.tipo_secundaria,
        'direccion_secundaria': solicitante.direccion_secundaria,
        'localidad_secundaria': solicitante.localidad_secundaria,
        'municipio_secundaria': solicitante.municipio_secundaria,
        'estado_secundaria': solicitante.estado_secundaria,
        'nombre_padre_tutor': solicitante.nombre_padre_tutor,
        'id_relacion_familiar': solicitante.id_relacion_familiar,
        'telefono_alumno': solicitante.telefono_alumno,
        'telefono_tutor': solicitante.telefono_tutor,
        'telefono_familiar': solicitante.telefono_familiar,
        'id_carrera_tecnica': solicitante.id_carrera_tecnica,
        'id_info_becas': solicitante.id_info_becas,
        'fecha_registro': solicitante.fecha_registro.strftime('%Y-%m-%d %H:%M:%S')
    } for solicitante in solicitantes]
    return jsonify(result), 200

