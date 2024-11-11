import os
import pandas as pd
from io import StringIO
from datetime import datetime
from flask import Blueprint,  jsonify, request, current_app as app
from Database.Database import TBL_ALUMNOS_AGREGADOS, TBL_CARRERAS_TECNICAS, TBL_CLINICAS, TBL_ESTADOS, TBL_GRADOS, TBL_GRUPOS, TBL_PAISES, TBL_SEXOS, TBL_USUARIOS, db, TBL_ALUMNOS, BITACORA_USUARIOS
from sqlalchemy.exc import SQLAlchemyError
from base64 import b64encode, b64decode

alumnos_bp = Blueprint('alumnos_bp', __name__)

# Ruta para insertar un nuevo alumno
@alumnos_bp.route('/alumno/insert', methods=['POST'])
def create_alumno():
    data = request.get_json()
    nombre_alumnos = data.get('nombre_alumnos')
    app_alumnos = data.get('app_alumnos')
    apm_alumnos = data.get('apm_alumnos')
    foto_alumnos = data.get('foto_alumnos')
    fecha_nacimiento_alumnos = data.get('fecha_nacimiento_alumnos')
    curp_alumnos = data.get('curp_alumnos')
    nocontrol_alumnos = data.get('nocontrol_alumnos')
    telefono_alumnos = data.get('telefono_alumnos')
    seguro_social_alumnos = data.get('seguro_social_alumnos')
    cuentacredencial_alumnos = data.get('cuentacredencial_alumnos')
    idSexo = data.get('idSexo')
    idUsuario = data.get('idUsuario')
    idClinica = data.get('idClinica')
    idGrado = data.get('idGrado')
    idGrupo = data.get('idGrupo')
    idTraslado = data.get('idTraslado')
    idTrasladotransporte = data.get('idTrasladotransporte')
    idCarreraTecnica = data.get('idCarreraTecnica')
    idPais = data.get('idPais')
    idEstado = data.get('idEstado')
    municipio_alumnos = data.get('municipio_alumnos')
    comunidad_alumnos = data.get('comunidad_alumnos')
    calle_alumnos = data.get('calle_alumnos')
    proc_sec_alumno = data.get('proc_sec_alumno')

    # Nuevos campos para el familiar del alumno
    nombre_completo_familiar = data.get('nombre_completo_familiar')
    telefono_familiar = data.get('telefono_familiar')
    telefono_trabajo_familiar = data.get('telefono_trabajo_familiar')
    correo_familiar = data.get('correo_familiar')

    # Validar campos obligatorios
    if not nombre_alumnos or not app_alumnos or not apm_alumnos or not fecha_nacimiento_alumnos or not curp_alumnos or not nocontrol_alumnos or not telefono_alumnos or not seguro_social_alumnos or not cuentacredencial_alumnos:
        return jsonify({'error': 'Los campos obligatorios no pueden estar vacíos'}), 400

    # Verificar si el idUsuario existe en TBL_USUARIOS
    usuario_existe = db.session.query(TBL_USUARIOS).filter_by(id_usuario=idUsuario).first()
    if not usuario_existe:
        return jsonify({'error': 'El ID de usuario no existe en TBL_USUARIOS'}), 400

    # Crear un nuevo alumno con los campos adicionales
    new_alumno = TBL_ALUMNOS(
        nombre_alumnos=nombre_alumnos,
        app_alumnos=app_alumnos,
        apm_alumnos=apm_alumnos,
        foto_alumnos=foto_alumnos,
        fecha_nacimiento_alumnos=fecha_nacimiento_alumnos,
        curp_alumnos=curp_alumnos,
        nocontrol_alumnos=nocontrol_alumnos,
        telefono_alumnos=telefono_alumnos,
        seguro_social_alumnos=seguro_social_alumnos,
        cuentacredencial_alumnos=cuentacredencial_alumnos,
        idSexo=idSexo,
        idUsuario=idUsuario,
        idClinica=idClinica,
        idGrado=idGrado,
        idGrupo=idGrupo,
        idTraslado=idTraslado,
        idTrasladotransporte=idTrasladotransporte,
        idCarreraTecnica=idCarreraTecnica,
        idPais=idPais,
        idEstado=idEstado,
        municipio_alumnos=municipio_alumnos,
        comunidad_alumnos=comunidad_alumnos,
        calle_alumnos=calle_alumnos,
        proc_sec_alumno=proc_sec_alumno,
        # Campos adicionales del familiar del alumno
        nombre_completo_familiar=nombre_completo_familiar,
        telefono_familiar=telefono_familiar,
        telefono_trabajo_familiar=telefono_trabajo_familiar,
        correo_familiar=correo_familiar
    )

    try:
        db.session.add(new_alumno)
        db.session.commit()

        # Insertar un nuevo registro en BITACORA_USUARIOS
        user_ip = request.remote_addr
        new_bitacora = BITACORA_USUARIOS(
            id_usuario=idUsuario,
            nombre_usuario=new_alumno.nombre_alumnos,
            accion_realizada='Registro',
            detalles_accion='Alumno registrado exitosamente',
            fecha_acceso=datetime.now(),
            ip_acceso=user_ip
        )
        db.session.add(new_bitacora)
        db.session.commit()

        return jsonify({'message': 'Alumno creado exitosamente'}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# Ruta para visualizar todos los alumnos con nombres relacionados
@alumnos_bp.route('/alumno', methods=['GET'])
def get_all_alumnos():
    alumnos = db.session.query(
        TBL_ALUMNOS,
        TBL_SEXOS.nombre_sexo,
        TBL_CLINICAS.nombre_clinicas,
        TBL_CARRERAS_TECNICAS.nombre_carrera_tecnica,
        TBL_CARRERAS_TECNICAS.foto_carrera_tecnica,
        TBL_GRADOS.nombre_grado,
        TBL_GRUPOS.nombre_grupos,
        TBL_PAISES.nombre_pais,
        TBL_ESTADOS.nombre_estado,
        TBL_USUARIOS.correo_usuario,
        TBL_USUARIOS.foto_usuario
    )\
    .join(TBL_SEXOS, TBL_ALUMNOS.idSexo == TBL_SEXOS.id_sexos)\
    .join(TBL_CLINICAS, TBL_ALUMNOS.idClinica == TBL_CLINICAS.id_clinicas)\
    .join(TBL_CARRERAS_TECNICAS, TBL_ALUMNOS.idCarreraTecnica == TBL_CARRERAS_TECNICAS.id_carrera_tecnica)\
    .join(TBL_GRADOS, TBL_ALUMNOS.idGrado == TBL_GRADOS.id_grado)\
    .join(TBL_GRUPOS, TBL_ALUMNOS.idGrupo == TBL_GRUPOS.id_grupos)\
    .join(TBL_PAISES, TBL_ALUMNOS.idPais == TBL_PAISES.id_pais)\
    .join(TBL_ESTADOS, TBL_ALUMNOS.idEstado == TBL_ESTADOS.id_estado)\
    .join(TBL_USUARIOS, TBL_ALUMNOS.idUsuario == TBL_USUARIOS.id_usuario)\
    .all()

    result = []
    for alumno in alumnos:
        alumno_data = alumno[0]
        nombre_sexo = alumno[1]
        nombre_clinica = alumno[2]
        nombre_carrera_tecnica = alumno[3]
        foto_carrera_tecnica = alumno[4]
        nombre_grado = alumno[5]
        nombre_grupo = alumno[6]
        nombre_pais = alumno[7]
        nombre_estado = alumno[8]
        correo_usuario = alumno[9]
        foto_usuario = alumno[10]

        result.append({
            'id_alumnos': alumno_data.id_alumnos,
            'nombre_alumnos': alumno_data.nombre_alumnos,
            'app_alumnos': alumno_data.app_alumnos,
            'apm_alumnos': alumno_data.apm_alumnos,
            'foto_usuario': b64encode(foto_usuario).decode('utf-8') if foto_usuario else None,
            'foto_carrera_tecnica': b64encode(foto_carrera_tecnica).decode('utf-8') if foto_carrera_tecnica else None,
            'fecha_nacimiento_alumnos': alumno_data.fecha_nacimiento_alumnos,
            'curp_alumnos': alumno_data.curp_alumnos,
            'nocontrol_alumnos': alumno_data.nocontrol_alumnos,
            'telefono_alumnos': alumno_data.telefono_alumnos,
            'seguro_social_alumnos': alumno_data.seguro_social_alumnos,
            'cuentacredencial_alumnos': alumno_data.cuentacredencial_alumnos,
            'sexo': nombre_sexo,
            'correo_usuario': correo_usuario,
            'clinica': nombre_clinica,
            'grado': nombre_grado,
            'grupo': nombre_grupo,
            'traslado': alumno_data.idTraslado,
            'traslado_transporte': alumno_data.idTrasladotransporte,
            'carrera_tecnica': nombre_carrera_tecnica,
            'pais': nombre_pais,
            'estado': nombre_estado,
            'municipio_alumnos': alumno_data.municipio_alumnos,
            'comunidad_alumnos': alumno_data.comunidad_alumnos,
            'calle_alumnos': alumno_data.calle_alumnos,
            'proc_sec_alumno': alumno_data.proc_sec_alumno,
            'nombre_completo_familiar': alumno_data.nombre_completo_familiar,
            'telefono_familiar': alumno_data.telefono_familiar,
            'telefono_trabajo_familiar': alumno_data.telefono_trabajo_familiar,
            'correo_familiar': alumno_data.correo_familiar
        })

    return jsonify(result), 200



# Ruta para visualizar un alumno por su ID
@alumnos_bp.route('/alumno/<int:id>', methods=['GET'])
def get_alumno(id):
    alumno = TBL_ALUMNOS.query.get(id)
    if not alumno:
        return jsonify({'error': 'Alumno no encontrado'}), 404
    return jsonify({
        'id_alumnos': alumno.id_alumnos,
        'nombre_alumnos': alumno.nombre_alumnos,
        'app_alumnos': alumno.app_alumnos,
        'apm_alumnos': alumno.apm_alumnos,
        'foto_alumnos': b64encode(alumno.foto_alumnos).decode('utf-8') if alumno.foto_alumnos else None,
        'fecha_nacimiento_alumnos': alumno.fecha_nacimiento_alumnos,
        'curp_alumnos': alumno.curp_alumnos,
        'nocontrol_alumnos': alumno.nocontrol_alumnos,
        'telefono_alumnos': alumno.telefono_alumnos,
        'seguro_social_alumnos': alumno.seguro_social_alumnos,
        'cuentacredencial_alumnos': alumno.cuentacredencial_alumnos,
        'idSexo': alumno.idSexo,
        'idUsuario': alumno.idUsuario,
        'idClinica': alumno.idClinica,
        'idGrado': alumno.idGrado,
        'idGrupo': alumno.idGrupo,
        'idTraslado': alumno.idTraslado,
        'idTrasladotransporte': alumno.idTrasladotransporte,
        'idCarreraTecnica': alumno.idCarreraTecnica,
        'idPais': alumno.idPais,
        'idEstado': alumno.idEstado,
        'municipio_alumnos': alumno.municipio_alumnos,
        'comunidad_alumnos': alumno.comunidad_alumnos,
        'calle_alumnos': alumno.calle_alumnos,
        'proc_sec_alumno': alumno.proc_sec_alumno,
        # Campos adicionales relacionados con el familiar del alumno
        'nombre_completo_familiar': alumno.nombre_completo_familiar,
        'telefono_familiar': alumno.telefono_familiar,
        'telefono_trabajo_familiar': alumno.telefono_trabajo_familiar,
        'correo_familiar': alumno.correo_familiar
    }), 200

# Ruta para actualizar un alumno por su ID
@alumnos_bp.route('/alumno-update/<int:id>', methods=['PUT'])
def update_alumno(id):
    data = request.get_json()
    alumno = TBL_ALUMNOS.query.get(id)

    if not alumno:
        return jsonify({'error': 'Alumno no encontrado'}), 404

    nombre_alumnos = data.get('nombre_alumnos')
    app_alumnos = data.get('app_alumnos')
    apm_alumnos = data.get('apm_alumnos')
    foto_alumnos = data.get('foto_alumnos')
    fecha_nacimiento_alumnos = data.get('fecha_nacimiento_alumnos')
    curp_alumnos = data.get('curp_alumnos')
    nocontrol_alumnos = data.get('nocontrol_alumnos')
    telefono_alumnos = data.get('telefono_alumnos')
    seguro_social_alumnos = data.get('seguro_social_alumnos')
    cuentacredencial_alumnos = data.get('cuentacredencial_alumnos')
    id_sexo = data.get('id_sexo')
    idUsuario = data.get('idUsuario')
    id_clinica = data.get('id_clinica')
    id_grado = data.get('id_grado')
    id_grupo = data.get('id_grupo')
    id_traslado = data.get('id_traslado')
    id_trasladotransporte = data.get('id_trasladotransporte')
    id_carrera_tecnica = data.get('id_carrera_tecnica')
    id_pais = data.get('id_pais')
    id_estado = data.get('id_estado')
    municipio_alumnos = data.get('municipio_alumnos')
    comunidad_alumnos = data.get('comunidad_alumnos')
    calle_alumnos = data.get('calle_alumnos')
    proc_sec_alumno = data.get('proc_sec_alumno')

    # Nuevos campos para actualizar la información del familiar del alumno
    nombre_completo_familiar = data.get('nombre_completo_familiar')
    telefono_familiar = data.get('telefono_familiar')
    telefono_trabajo_familiar = data.get('telefono_trabajo_familiar')
    correo_familiar = data.get('correo_familiar')

    if not nombre_alumnos or not app_alumnos or not apm_alumnos or not fecha_nacimiento_alumnos or not curp_alumnos or not nocontrol_alumnos or not telefono_alumnos or not seguro_social_alumnos or not cuentacredencial_alumnos:
        return jsonify({'error': 'Los campos obligatorios no pueden estar vacíos'}), 400

    # Actualizar los campos del alumno
    alumno.nombre_alumnos = nombre_alumnos
    alumno.app_alumnos = app_alumnos
    alumno.apm_alumnos = apm_alumnos
    if foto_alumnos:
        alumno.foto_alumnos = b64decode(foto_alumnos.encode('utf-8'))
    alumno.fecha_nacimiento_alumnos = fecha_nacimiento_alumnos
    alumno.curp_alumnos = curp_alumnos
    alumno.nocontrol_alumnos = nocontrol_alumnos
    alumno.telefono_alumnos = telefono_alumnos
    alumno.seguro_social_alumnos = seguro_social_alumnos
    alumno.cuentacredencial_alumnos = cuentacredencial_alumnos
    alumno.id_sexo = id_sexo
    alumno.idUsuario = idUsuario
    alumno.id_clinica = id_clinica
    alumno.id_grado = id_grado
    alumno.id_grupo = id_grupo
    alumno.id_traslado = id_traslado
    alumno.id_trasladotransporte = id_trasladotransporte
    alumno.id_carrera_tecnica = id_carrera_tecnica
    alumno.id_pais = id_pais
    alumno.id_estado = id_estado
    alumno.municipio_alumnos = municipio_alumnos
    alumno.comunidad_alumnos = comunidad_alumnos
    alumno.calle_alumnos = calle_alumnos
    alumno.proc_sec_alumno = proc_sec_alumno

    # Actualizar los campos del familiar del alumno
    alumno.nombre_completo_familiar = nombre_completo_familiar
    alumno.telefono_familiar = telefono_familiar
    alumno.telefono_trabajo_familiar = telefono_trabajo_familiar
    alumno.correo_familiar = correo_familiar

    try:
        db.session.commit()

        # Insertar un nuevo registro en BITACORA_USUARIOS
        user_ip = request.remote_addr
        new_bitacora = BITACORA_USUARIOS(
            id_usuario=idUsuario,
            nombre_usuario=alumno.nombre_alumnos,
            accion_realizada='Actualización',
            detalles_accion='Alumno actualizado exitosamente',
            fecha_acceso=datetime.now(),
            ip_acceso=user_ip
        )
        db.session.add(new_bitacora)
        db.session.commit()

        return jsonify({'message': 'Alumno actualizado exitosamente'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# Ruta para eliminar un alumno por su ID
@alumnos_bp.route('/alumno/<int:id>', methods=['DELETE'])
def delete_alumno(id):
    alumno = TBL_ALUMNOS.query.get(id)
    if not alumno:
        return jsonify({'error': 'Alumno no encontrado'}), 404

    try:
        db.session.delete(alumno)
        db.session.commit()

        # Insertar un nuevo registro en BITACORA_USUARIOS
        user_ip = request.remote_addr
        new_bitacora = BITACORA_USUARIOS(
            id_usuario=alumno.id_usuario,
            nombre_usuario=alumno.nombre_alumnos,
            accion_realizada='Eliminación',
            detalles_accion='Alumno eliminado exitosamente',
            fecha_acceso=datetime.now(),
            ip_acceso=user_ip
        )
        db.session.add(new_bitacora)
        db.session.commit()

        return jsonify({'message': 'Alumno eliminado exitosamente'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Ruta para buscar un alumno por su número de control
@alumnos_bp.route('/alumnos/nocontrol/<string:nocontrol>', methods=['GET'])
def get_alumno_by_nocontrol(nocontrol):
    alumno = db.session.query(
        TBL_ALUMNOS, 
        TBL_SEXOS.nombre_sexo, 
        TBL_CLINICAS.nombre_clinicas, 
        TBL_CARRERAS_TECNICAS.nombre_carrera_tecnica,
        TBL_CARRERAS_TECNICAS.foto_carrera_tecnica,  # Incluir foto de la carrera técnica
        TBL_GRADOS.nombre_grado,
        TBL_GRUPOS.nombre_grupos,
        TBL_PAISES.nombre_pais,
        TBL_ESTADOS.nombre_estado,
        TBL_USUARIOS.correo_usuario,
        TBL_USUARIOS.foto_usuario  # Incluir foto del usuario
    )\
    .join(TBL_SEXOS, TBL_ALUMNOS.idSexo == TBL_SEXOS.id_sexos)\
    .join(TBL_CLINICAS, TBL_ALUMNOS.idClinica == TBL_CLINICAS.id_clinicas)\
    .join(TBL_CARRERAS_TECNICAS, TBL_ALUMNOS.idCarreraTecnica == TBL_CARRERAS_TECNICAS.id_carrera_tecnica)\
    .join(TBL_GRADOS, TBL_ALUMNOS.idGrado == TBL_GRADOS.id_grado)\
    .join(TBL_GRUPOS, TBL_ALUMNOS.idGrupo == TBL_GRUPOS.id_grupos)\
    .join(TBL_PAISES, TBL_ALUMNOS.idPais == TBL_PAISES.id_pais)\
    .join(TBL_ESTADOS, TBL_ALUMNOS.idEstado == TBL_ESTADOS.id_estado)\
    .join(TBL_USUARIOS, TBL_ALUMNOS.idUsuario == TBL_USUARIOS.id_usuario)\
    .filter(TBL_ALUMNOS.nocontrol_alumnos == nocontrol).first()

    if not alumno:
        return jsonify({'error': 'Alumno no encontrado'}), 404

    alumno_data = alumno[0]
    nombre_sexo = alumno[1]
    nombre_clinica = alumno[2]
    nombre_carrera_tecnica = alumno[3]
    foto_carrera_tecnica = alumno[4]  # Foto de la carrera técnica
    nombre_grado = alumno[5]
    nombre_grupo = alumno[6]
    nombre_pais = alumno[7]
    nombre_estado = alumno[8]
    correo_usuario = alumno[9]
    foto_usuario = alumno[10]  # Foto del usuario

    return jsonify({
        'id_alumnos': alumno_data.id_alumnos,
        'nombre_alumnos': alumno_data.nombre_alumnos,
        'app_alumnos': alumno_data.app_alumnos,
        'apm_alumnos': alumno_data.apm_alumnos,
        'foto_usuario': b64encode(foto_usuario).decode('utf-8') if foto_usuario else None,  # Utilizar foto del usuario
        'foto_carrera_tecnica': b64encode(foto_carrera_tecnica).decode('utf-8') if foto_carrera_tecnica else None,  # Utilizar foto de la carrera técnica
        'fecha_nacimiento_alumnos': alumno_data.fecha_nacimiento_alumnos,
        'curp_alumnos': alumno_data.curp_alumnos,
        'nocontrol_alumnos': alumno_data.nocontrol_alumnos,
        'telefono_alumnos': alumno_data.telefono_alumnos,
        'seguro_social_alumnos': alumno_data.seguro_social_alumnos,
        'cuentacredencial_alumnos': alumno_data.cuentacredencial_alumnos,
        'sexo': nombre_sexo,
        'correo_usuario': correo_usuario,
        'clinica': nombre_clinica,
        'grado': nombre_grado,
        'grupo': nombre_grupo,
        'traslado': alumno_data.idTraslado,
        'traslado_transporte': alumno_data.idTrasladotransporte,
        'carrera_tecnica': nombre_carrera_tecnica,
        'pais': nombre_pais,
        'estado': nombre_estado,
        'municipio_alumnos': alumno_data.municipio_alumnos,
        'comunidad_alumnos': alumno_data.comunidad_alumnos,
        'calle_alumnos': alumno_data.calle_alumnos,
        'proc_sec_alumno': alumno_data.proc_sec_alumno,
        # Campos adicionales del familiar del alumno
        'nombre_completo_familiar': alumno_data.nombre_completo_familiar,
        'telefono_familiar': alumno_data.telefono_familiar,
        'telefono_trabajo_familiar': alumno_data.telefono_trabajo_familiar,
        'correo_familiar': alumno_data.correo_familiar
    }), 200



# Ruta para obtener la información del alumno relacionado con el usuario logueado
@alumnos_bp.route('/alumno/usuario/<int:id_usuario>', methods=['GET'])
def get_alumno_by_usuario(id_usuario):
    alumno = db.session.query(
        TBL_ALUMNOS, 
        TBL_SEXOS.nombre_sexo, 
        TBL_CLINICAS.nombre_clinicas, 
        TBL_CARRERAS_TECNICAS.nombre_carrera_tecnica,
        TBL_CARRERAS_TECNICAS.foto_carrera_tecnica,  # Añadir foto de la carrera técnica
        TBL_GRADOS.nombre_grado,
        TBL_GRUPOS.nombre_grupos,
        TBL_PAISES.nombre_pais,
        TBL_ESTADOS.nombre_estado,
        TBL_USUARIOS.foto_usuario  # Añadir foto del usuario
    )\
    .join(TBL_SEXOS, TBL_ALUMNOS.idSexo == TBL_SEXOS.id_sexos)\
    .join(TBL_CLINICAS, TBL_ALUMNOS.idClinica == TBL_CLINICAS.id_clinicas)\
    .join(TBL_CARRERAS_TECNICAS, TBL_ALUMNOS.idCarreraTecnica == TBL_CARRERAS_TECNICAS.id_carrera_tecnica)\
    .join(TBL_GRADOS, TBL_ALUMNOS.idGrado == TBL_GRADOS.id_grado)\
    .join(TBL_GRUPOS, TBL_ALUMNOS.idGrupo == TBL_GRUPOS.id_grupos)\
    .join(TBL_PAISES, TBL_ALUMNOS.idPais == TBL_PAISES.id_pais)\
    .join(TBL_ESTADOS, TBL_ALUMNOS.idEstado == TBL_ESTADOS.id_estado)\
    .join(TBL_USUARIOS, TBL_ALUMNOS.idUsuario == TBL_USUARIOS.id_usuario)\
    .filter(TBL_ALUMNOS.idUsuario == id_usuario).first()
        
    if not alumno:
        return jsonify({'error': 'Alumno no encontrado'}), 404
    
    alumno_data = alumno[0]  # Datos del alumno
    nombre_sexo = alumno[1]  # Nombre del sexo
    nombre_clinica = alumno[2]  # Nombre de la clínica
    nombre_carrera_tecnica = alumno[3]  # Nombre de la carrera técnica
    foto_carrera_tecnica = alumno[4]  # Foto de la carrera técnica
    nombre_grado = alumno[5]  # Nombre del grado
    nombre_grupo = alumno[6]  # Nombre del grupo
    nombre_pais = alumno[7]  # Nombre del país
    nombre_estado = alumno[8]  # Nombre del estado
    foto_usuario = alumno[9]  # Foto del usuario

    return jsonify({
        'id_alumnos': alumno_data.id_alumnos,
        'nombre_alumnos': alumno_data.nombre_alumnos,
        'app_alumnos': alumno_data.app_alumnos,
        'apm_alumnos': alumno_data.apm_alumnos,
        'foto_alumnos': b64encode(foto_usuario).decode('utf-8') if foto_usuario else None,
        'fecha_nacimiento_alumnos': alumno_data.fecha_nacimiento_alumnos,
        'curp_alumnos': alumno_data.curp_alumnos,
        'nocontrol_alumnos': alumno_data.nocontrol_alumnos,
        'telefono_alumnos': alumno_data.telefono_alumnos,
        'seguro_social_alumnos': alumno_data.seguro_social_alumnos,
        'cuentacredencial_alumnos': alumno_data.cuentacredencial_alumnos,
        'sexo': nombre_sexo,  # Incluye el nombre del sexo en la respuesta
        'clinica': nombre_clinica,  # Incluye el nombre de la clínica en la respuesta
        'carrera_tecnica': nombre_carrera_tecnica,  # Incluye el nombre de la carrera técnica en la respuesta
        'foto_carrera_tecnica': b64encode(foto_carrera_tecnica).decode('utf-8') if foto_carrera_tecnica else None,  # Foto de la carrera técnica
        'grado': nombre_grado,  # Incluye el nombre del grado en la respuesta
        'grupo': nombre_grupo,  # Incluye el nombre del grupo en la respuesta
        'pais': nombre_pais,  # Incluye el nombre del país en la respuesta
        'estado': nombre_estado,  # Incluye el nombre del estado en la respuesta
        'idUsuario': alumno_data.idUsuario,
        'idTraslado': alumno_data.idTraslado,
        'idTrasladotransporte': alumno_data.idTrasladotransporte,
        'municipio_alumnos': alumno_data.municipio_alumnos,
        'comunidad_alumnos': alumno_data.comunidad_alumnos,
        'calle_alumnos': alumno_data.calle_alumnos,
        'proc_sec_alumno': alumno_data.proc_sec_alumno,
        # Campos adicionales del familiar del alumno
        'nombre_completo_familiar': alumno_data.nombre_completo_familiar,
        'telefono_familiar': alumno_data.telefono_familiar,
        'telefono_trabajo_familiar': alumno_data.telefono_trabajo_familiar,
        'correo_familiar': alumno_data.correo_familiar
    }), 200


@alumnos_bp.route('/alumno/alexa/usuario/<int:id>', methods=['GET'])
def get_alumno_por_usuario_alexa(id):
    alumno = TBL_ALUMNOS.query.filter_by(idUsuario=id).first()
    if not alumno:
        return jsonify({'error': 'Alumno no encontrado'}), 404
    return jsonify({
        'id_alumnos': alumno.id_alumnos,
        'nombre_alumnos': alumno.nombre_alumnos,
        'app_alumnos': alumno.app_alumnos,
        'apm_alumnos': alumno.apm_alumnos,
        'foto_alumnos': b64encode(alumno.foto_alumnos).decode('utf-8') if alumno.foto_alumnos else None,
        'fecha_nacimiento_alumnos': alumno.fecha_nacimiento_alumnos,
        'curp_alumnos': alumno.curp_alumnos,
        'nocontrol_alumnos': alumno.nocontrol_alumnos,
        'telefono_alumnos': alumno.telefono_alumnos,
        'seguro_social_alumnos': alumno.seguro_social_alumnos,
        'cuentacredencial_alumnos': alumno.cuentacredencial_alumnos,
        'idSexo': alumno.idSexo,
        'idUsuario': alumno.idUsuario,
        'idClinica': alumno.idClinica,
        'idGrado': alumno.idGrado,
        'idGrupo': alumno.idGrupo,
        'idTraslado': alumno.idTraslado,
        'idTrasladotransporte': alumno.idTrasladotransporte,
        'idCarreraTecnica': alumno.idCarreraTecnica,
        'idPais': alumno.idPais,
        'idEstado': alumno.idEstado,
        'municipio_alumnos': alumno.municipio_alumnos,
        'comunidad_alumnos': alumno.comunidad_alumnos,
        'calle_alumnos': alumno.calle_alumnos,
        'proc_sec_alumno': alumno.proc_sec_alumno,
        # Campos adicionales relacionados con el familiar del alumno
        'nombre_completo_familiar': alumno.nombre_completo_familiar,
        'telefono_familiar': alumno.telefono_familiar,
        'telefono_trabajo_familiar': alumno.telefono_trabajo_familiar,
        'correo_familiar': alumno.correo_familiar
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


@alumnos_bp.route('/alumno/upload_csv', methods=['POST'])
def upload_csv():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        try:
            df = pd.read_csv(file)
            
            # Depuración: imprimir nombres de columnas
            print("Columnas del DataFrame:", df.columns)

            required_columns = [
                'nombre_alumnos', 'app_alumnos', 'apm_alumnos', 'fecha_nacimiento_alumnos',
                'curp_alumnos', 'nocontrol_alumnos', 'telefono_alumnos', 'seguro_social_alumnos',
                'cuentacredencial_alumnos', 'idSexo', 'idUsuario', 'idClinica', 'idGrado', 'idGrupo',
                'idTraslado', 'idTrasladotransporte', 'idCarreraTecnica', 'idPais', 'idEstado',
                'municipio_alumnos', 'comunidad_alumnos', 'calle_alumnos', 'proc_sec_alumno',
                # Nuevos campos del familiar del alumno
                'nombre_completo_familiar', 'telefono_familiar', 'telefono_trabajo_familiar', 'correo_familiar'
            ]

            for column in required_columns:
                if column not in df.columns:
                    return jsonify({'error': f'Missing required column: {column}'}), 400

            df['fecha_nacimiento_alumnos'] = df['fecha_nacimiento_alumnos'].apply(lambda x: parse_date(str(x)))

            if df['fecha_nacimiento_alumnos'].isnull().any():
                return jsonify({'error': 'Invalid date format in fecha_nacimiento_alumnos column'}), 400

            with db.session.no_autoflush:
                for _, row in df.iterrows():
                    # Depuración: imprimir valor de idUsuario
                    print("Verificando idUsuario:", row['idUsuario'])
                    
                    # Verificar si el idUsuario existe en la tabla TBL_USUARIOS
                    usuario_existente = TBL_USUARIOS.query.filter_by(id_usuario=row['idUsuario']).first()
                    if not usuario_existente:
                        return jsonify({'error': f'Invalid idUsuario: {row["idUsuario"]}'}), 400

                    # Verificar si el registro ya existe
                    existing_alumno = TBL_ALUMNOS.query.filter_by(nocontrol_alumnos=row['nocontrol_alumnos']).first()
                    if existing_alumno:
                        continue  # Saltar el registro si ya existe

                    new_alumno = TBL_ALUMNOS(
                        nombre_alumnos=row['nombre_alumnos'],
                        app_alumnos=row['app_alumnos'],
                        apm_alumnos=row['apm_alumnos'],
                        fecha_nacimiento_alumnos=row['fecha_nacimiento_alumnos'],
                        curp_alumnos=row['curp_alumnos'],
                        nocontrol_alumnos=row['nocontrol_alumnos'],
                        telefono_alumnos=row['telefono_alumnos'],
                        seguro_social_alumnos=row['seguro_social_alumnos'],
                        cuentacredencial_alumnos=row['cuentacredencial_alumnos'],
                        idSexo=row['idSexo'],
                        idUsuario=row['idUsuario'],
                        idClinica=row['idClinica'],
                        idGrado=row['idGrado'],
                        idGrupo=row['idGrupo'],
                        idTraslado=row['idTraslado'],
                        idTrasladotransporte=row['idTrasladotransporte'],
                        idCarreraTecnica=row['idCarreraTecnica'],
                        idPais=row['idPais'],
                        idEstado=row['idEstado'],
                        municipio_alumnos=row['municipio_alumnos'],
                        comunidad_alumnos=row['comunidad_alumnos'],
                        calle_alumnos=row['calle_alumnos'],
                        proc_sec_alumno=row['proc_sec_alumno'],
                        # Nuevos campos del familiar del alumno
                        nombre_completo_familiar=row['nombre_completo_familiar'],
                        telefono_familiar=row['telefono_familiar'],
                        telefono_trabajo_familiar=row['telefono_trabajo_familiar'],
                        correo_familiar=row['correo_familiar']
                    )
                    db.session.add(new_alumno)
                db.session.commit()

            return jsonify({'message': 'Archivo CSV subido exitosamente'}), 201
        except Exception as e:
            # Depuración: imprimir excepción completa
            import traceback
            print("Error procesando el archivo CSV:", traceback.format_exc())
            return jsonify({'error': str(e)}), 500
    return jsonify({'error': 'Invalid file'}), 400


#aqui es del lado familiar 
@alumnos_bp.route('/alumnos_agregados/view/<int:id_usuario>', methods=['GET'])
def get_alumnos_agregados(id_usuario):
    try:
        alumnos_agregados = TBL_ALUMNOS_AGREGADOS.query.filter_by(id_usuario=id_usuario).all()
        result = []

        for agregado in alumnos_agregados:
            alumno = db.session.query(
                TBL_ALUMNOS,
                TBL_SEXOS.nombre_sexo,
                TBL_CLINICAS.nombre_clinicas,
                TBL_CARRERAS_TECNICAS.nombre_carrera_tecnica,
                TBL_CARRERAS_TECNICAS.foto_carrera_tecnica,
                TBL_GRADOS.nombre_grado,
                TBL_GRUPOS.nombre_grupos,
                TBL_PAISES.nombre_pais,
                TBL_ESTADOS.nombre_estado,
                TBL_USUARIOS.correo_usuario,
                TBL_USUARIOS.foto_usuario
            ).join(TBL_SEXOS, TBL_ALUMNOS.idSexo == TBL_SEXOS.id_sexos) \
             .join(TBL_CLINICAS, TBL_ALUMNOS.idClinica == TBL_CLINICAS.id_clinicas) \
             .join(TBL_CARRERAS_TECNICAS, TBL_ALUMNOS.idCarreraTecnica == TBL_CARRERAS_TECNICAS.id_carrera_tecnica) \
             .join(TBL_GRADOS, TBL_ALUMNOS.idGrado == TBL_GRADOS.id_grado) \
             .join(TBL_GRUPOS, TBL_ALUMNOS.idGrupo == TBL_GRUPOS.id_grupos) \
             .join(TBL_PAISES, TBL_ALUMNOS.idPais == TBL_PAISES.id_pais) \
             .join(TBL_ESTADOS, TBL_ALUMNOS.idEstado == TBL_ESTADOS.id_estado) \
             .join(TBL_USUARIOS, TBL_ALUMNOS.idUsuario == TBL_USUARIOS.id_usuario) \
             .filter(TBL_ALUMNOS.id_alumnos == agregado.id_alumno).first()

            if alumno:
                alumno_data = alumno[0]
                nombre_sexo = alumno[1]
                nombre_clinica = alumno[2]
                nombre_carrera_tecnica = alumno[3]
                foto_carrera_tecnica = alumno[4]
                nombre_grado = alumno[5]
                nombre_grupo = alumno[6]
                nombre_pais = alumno[7]
                nombre_estado = alumno[8]
                correo_usuario = alumno[9]
                foto_usuario = alumno[10]

                result.append({
                    'id_alumnos': alumno_data.id_alumnos,
                    'nombre_alumnos': alumno_data.nombre_alumnos,
                    'app_alumnos': alumno_data.app_alumnos,
                    'apm_alumnos': alumno_data.apm_alumnos,
                    'foto_usuario': b64encode(foto_usuario).decode('utf-8') if foto_usuario else None,
                    'foto_carrera_tecnica': b64encode(foto_carrera_tecnica).decode('utf-8') if foto_carrera_tecnica else None,
                    'fecha_nacimiento_alumnos': alumno_data.fecha_nacimiento_alumnos,
                    'curp_alumnos': alumno_data.curp_alumnos,
                    'nocontrol_alumnos': alumno_data.nocontrol_alumnos,
                    'telefono_alumnos': alumno_data.telefono_alumnos,
                    'seguro_social_alumnos': alumno_data.seguro_social_alumnos,
                    'cuentacredencial_alumnos': alumno_data.cuentacredencial_alumnos,
                    'sexo': nombre_sexo,
                    'correo_usuario': correo_usuario,
                    'clinica': nombre_clinica,
                    'grado': nombre_grado,
                    'grupo': nombre_grupo,
                    'traslado': alumno_data.idTraslado,
                    'traslado_transporte': alumno_data.idTrasladotransporte,
                    'carrera_tecnica': nombre_carrera_tecnica,
                    'pais': nombre_pais,
                    'estado': nombre_estado,
                    'municipio_alumnos': alumno_data.municipio_alumnos,
                    'comunidad_alumnos': alumno_data.comunidad_alumnos,
                    'calle_alumnos': alumno_data.calle_alumnos,
                    'proc_sec_alumno': alumno_data.proc_sec_alumno,
                    # Campos adicionales del familiar del alumno
                    'nombre_completo_familiar': alumno_data.nombre_completo_familiar,
                    'telefono_familiar': alumno_data.telefono_familiar,
                    'telefono_trabajo_familiar': alumno_data.telefono_trabajo_familiar,
                    'correo_familiar': alumno_data.correo_familiar
                })

        return jsonify(result), 200
    except SQLAlchemyError as e:
        return jsonify({'error': 'Error al obtener alumnos agregados: ' + str(e)}), 500




@alumnos_bp.route('/alumnos_agregados/add', methods=['POST'])
def add_alumno_agregado():
    data = request.get_json()
    id_usuario = data.get('id_usuario')
    id_alumno = data.get('id_alumno')

    if not id_usuario or not id_alumno:
        return jsonify({'error': 'Faltan datos'}), 400

    nuevo_alumno_agregado = TBL_ALUMNOS_AGREGADOS(
        id_usuario=id_usuario,
        id_alumno=id_alumno
    )

    try:
        db.session.add(nuevo_alumno_agregado)
        db.session.commit()
        return jsonify({'message': 'Alumno agregado exitosamente'}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Error al agregar alumno: ' + str(e)}), 500


@alumnos_bp.route('/alumnos_agregados/delete', methods=['DELETE'])
def delete_alumno_agregado():
    data = request.get_json()
    id_usuario = data.get('id_usuario')
    id_alumno = data.get('id_alumno')

    if not id_usuario or not id_alumno:
        return jsonify({'error': 'Faltan datos en la solicitud'}), 400

    alumno_agregado = TBL_ALUMNOS_AGREGADOS.query.filter_by(id_usuario=id_usuario, id_alumno=id_alumno).first()
    if not alumno_agregado:
        return jsonify({'error': 'Alumno agregado no encontrado'}), 404

    try:
        db.session.delete(alumno_agregado)
        db.session.commit()
        return jsonify({'message': 'Alumno eliminado exitosamente'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
