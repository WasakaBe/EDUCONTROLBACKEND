from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.types import JSON

db = SQLAlchemy()

# Clases Principales de la base de datos
class TBL_TIPO_ROL(db.Model):
    id_tipo_rol = db.Column(db.Integer, primary_key=True)
    nombre_tipo_rol = db.Column(db.String(30), nullable=False, unique=True)

class TBL_SEXOS(db.Model):
    id_sexos = db.Column(db.Integer, primary_key=True)
    nombre_sexo = db.Column(db.String(30), nullable=False, unique=True)

class TBL_ACTIVOS_CUENTAS(db.Model):
    id_activos_cuenta = db.Column(db.Integer, primary_key=True)
    nombre_activos_cuenta = db.Column(db.String(30), nullable=False, unique=True)

class TBL_TRASLADO(db.Model):
    id_traslado = db.Column(db.Integer, primary_key=True)
    nombre_traslado = db.Column(db.String(20), nullable=False, unique=True)
 
class TBL_TRASLADO_TRANSPORTE(db.Model):
    id_traslado_transporte = db.Column(db.Integer, primary_key=True)
    nombre_traslado_transporte = db.Column(db.String(20), nullable=False, unique=True)

class TBL_ASIGNATURAS(db.Model):
    id_asignatura = db.Column(db.Integer, primary_key=True)
    nombre_asignatura = db.Column(db.String(40), nullable=False, unique=True)

class TBL_GRADOS(db.Model):
    id_grado = db.Column(db.Integer, primary_key=True)
    nombre_grado = db.Column(db.Integer, nullable=False, unique=True)
 
class TBL_GRUPOS(db.Model):
    id_grupos = db.Column(db.Integer, primary_key=True)
    nombre_grupos = db.Column(db.String(3), nullable=False, unique=True)

class TBL_PREGUNTAS(db.Model):
    id_preguntas = db.Column(db.Integer, primary_key=True)
    nombre_preguntas = db.Column(db.String(100), nullable=False, unique=True)

class TBL_CARRERAS_TECNICAS(db.Model):
    id_carrera_tecnica = db.Column(db.Integer, primary_key=True)
    nombre_carrera_tecnica = db.Column(db.String(200), nullable=False, unique=True)
    descripcion_carrera_tecnica = db.Column(db.Text, nullable=False)
    foto_carrera_tecnica = db.Column(db.LargeBinary)

class TBL_CLINICAS(db.Model):
    id_clinicas = db.Column(db.Integer, primary_key=True)
    nombre_clinicas = db.Column(db.String(100), nullable=False, unique=True)

class TBL_PAISES(db.Model):
    id_pais = db.Column(db.Integer, primary_key=True)
    nombre_pais = db.Column(db.String(250), nullable=False, unique=True)
    foto_pais = db.Column(db.LargeBinary)

class TBL_ESTADOS(db.Model):
    id_estado = db.Column(db.Integer, primary_key=True)
    nombre_estado = db.Column(db.String(250), nullable=False, unique=True)
    foto_estado = db.Column(db.LargeBinary)

class TBL_RELACION_FAMILIAR(db.Model):
    id_relacion_familiar = db.Column(db.Integer, primary_key=True)
    nombre_relacion_familiar = db.Column(db.String(50), nullable=False, unique=True)

class TBL_MOTIVO_CREDENCIAL(db.Model):
    id_motivo_credencial = db.Column(db.Integer, primary_key=True)
    nombre_motivo_credencial = db.Column(db.String(50), nullable=False, unique=True)

class TBL_CARRUSEL_IMG(db.Model):
    id_carrusel = db.Column(db.Integer, primary_key=True)
    carrusel = db.Column(db.LargeBinary)

class TBL_MENSAJES_CONTACTOS(db.Model):
    id_mensaje_contacto = db.Column(db.Integer, primary_key=True)
    nombre_mensaje_contacto = db.Column(db.String(50), nullable=False)
    correo_mensaje_contacto = db.Column(db.String(50), nullable=False)
    motivo_mensaje_contacto = db.Column(db.Text)
    fecha_mensaje = db.Column(db.DateTime)

# Clases Llaves Foráneas de la base de datos
class TBL_USUARIOS(db.Model):
    id_usuario = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(100), nullable=False)
    app_usuario = db.Column(db.String(100), nullable=False)
    apm_usuario = db.Column(db.String(100))
    fecha_nacimiento_usuario = db.Column(db.DateTime)
    token_usuario = db.Column(db.String(8), nullable=False)
    correo_usuario = db.Column(db.String(50), nullable=False, unique=True)
    pwd_usuario = db.Column(db.String(20), nullable=False)
    phone_usuario = db.Column(db.BigInteger)
    ip_usuario = db.Column(db.String(50), nullable=False)
    idRol = db.Column(db.Integer, db.ForeignKey('tbl_tipo_rol.id_tipo_rol'))
    idSexo = db.Column(db.Integer, db.ForeignKey('tbl_sexos.id_sexos'))
    idCuentaActivo = db.Column(db.Integer, db.ForeignKey('tbl_activos_cuentas.id_activos_cuenta'))
    idPregunta = db.Column(db.Integer, db.ForeignKey('tbl_preguntas.id_preguntas'))
    respuestaPregunta = db.Column(db.String(255))
    foto_usuario = db.Column(db.LargeBinary)

class TBL_DOCENTES(db.Model):
    id_docentes = db.Column(db.Integer, primary_key=True)
    nombre_docentes = db.Column(db.String(50), nullable=False)
    app_docentes = db.Column(db.String(50), nullable=False)
    apm_docentes = db.Column(db.String(50), nullable=False)
    fecha_nacimiento_docentes = db.Column(db.DateTime, nullable=False)
    noconttrol_docentes = db.Column(db.BigInteger, nullable=False, unique=True)
    telefono_docentes = db.Column(db.BigInteger, nullable=False, unique=True)
    foto_docentes = db.Column(db.LargeBinary)
    seguro_social_docentes = db.Column(db.BigInteger, nullable=False, unique=True)
    idSexo = db.Column(db.Integer, db.ForeignKey('tbl_sexos.id_sexos'))
    idUsuario = db.Column(db.Integer, db.ForeignKey('tbl_usuarios.id_usuario'))
    idClinica = db.Column(db.Integer, db.ForeignKey('tbl_clinicas.id_clinicas'))

class TBL_ALUMNOS(db.Model):
    id_alumnos = db.Column(db.Integer, primary_key=True)
    nombre_alumnos = db.Column(db.String(100), nullable=False)
    app_alumnos = db.Column(db.String(100), nullable=False)
    apm_alumnos = db.Column(db.String(100), nullable=False)
    foto_alumnos = db.Column(db.LargeBinary)
    fecha_nacimiento_alumnos = db.Column(db.DateTime, nullable=False)
    curp_alumnos = db.Column(db.String(50), nullable=False, unique=True)
    nocontrol_alumnos = db.Column(db.BigInteger, nullable=False, unique=True)
    telefono_alumnos = db.Column(db.BigInteger, nullable=False, unique=True)
    seguro_social_alumnos = db.Column(db.BigInteger, nullable=False, unique=True)
    cuentacredencial_alumnos = db.Column(db.String(2), nullable=False)
    idSexo = db.Column(db.Integer, db.ForeignKey('tbl_sexos.id_sexos'))
    idUsuario = db.Column(db.Integer, db.ForeignKey('tbl_usuarios.id_usuario'))
    idClinica = db.Column(db.Integer, db.ForeignKey('tbl_clinicas.id_clinicas'))
    idGrado = db.Column(db.Integer, db.ForeignKey('tbl_grados.id_grado'))
    idGrupo = db.Column(db.Integer, db.ForeignKey('tbl_grupos.id_grupos'))
    idTraslado = db.Column(db.Integer, db.ForeignKey('tbl_traslado.id_traslado'))
    idTrasladotransporte = db.Column(db.Integer, db.ForeignKey('tbl_traslado_transporte.id_traslado_transporte'))
    idCarreraTecnica = db.Column(db.Integer, db.ForeignKey('tbl_carreras_tecnicas.id_carrera_tecnica'))
    idPais = db.Column(db.Integer, db.ForeignKey('tbl_paises.id_pais'))
    idEstado = db.Column(db.Integer, db.ForeignKey('tbl_estados.id_estado'))
    municipio_alumnos = db.Column(db.String(100), nullable=False)
    comunidad_alumnos = db.Column(db.String(100), nullable=False)
    calle_alumnos = db.Column(db.String(100), nullable=False)
    proc_sec_alumno = db.Column(db.String(100), nullable=False)
        # Nuevos campos relacionados con el familiar del alumno
    nombre_completo_familiar = db.Column(db.String(100), nullable=False)
    telefono_familiar = db.Column(db.BigInteger, nullable=False)
    telefono_trabajo_familiar = db.Column(db.BigInteger, nullable=False)
    correo_familiar = db.Column(db.String(100), nullable=False)

class TBL_MENSAJES_MOTIVO_CREDENCIAL(db.Model):
    id_mensajes_motivo_credencial = db.Column(db.Integer, primary_key=True)
    idalumno = db.Column(db.Integer, db.ForeignKey('tbl_alumnos.id_alumnos'))
    idmotivo = db.Column(db.Integer, db.ForeignKey('tbl_motivo_credencial.id_motivo_credencial'))
    fecha_motivo_credencial = db.Column(db.DateTime)

class TBL_CREDENCIALES_ESCOLARES(db.Model):
    id_credencial_escolar = db.Column(db.Integer, primary_key=True)
    nombre_credencial_escolar = db.Column(db.String(100))
    app_credencial_escolar = db.Column(db.String(100))
    apm_credencial_escolar = db.Column(db.String(100))
    carrera_credencial_escolar = db.Column(db.String(100))
    grupo_credencial_escolar = db.Column(db.String(2))
    curp_credencial_escolar = db.Column(db.String(22))
    nocontrol_credencial_escolar = db.Column(db.String(22))
    segsocial_credencial_escolar = db.Column(db.String(22))
    foto_credencial_escolar = db.Column(db.LargeBinary)
    idalumnocrede = db.Column(db.Integer, db.ForeignKey('tbl_alumnos.id_alumnos'))

class TBL_WELCOME(db.Model):
    id_welcome = db.Column(db.Integer, primary_key=True)
    welcome_text = db.Column(db.Text)
    foto_welcome = db.Column(db.LargeBinary)

class TBL_MISION(db.Model):
    id_mision = db.Column(db.Integer, primary_key=True)
    mision_text = db.Column(db.Text)

class TBL_VISION(db.Model):
    id_vision = db.Column(db.Integer, primary_key=True)
    vision_text = db.Column(db.Text)

class BITACORA_USUARIOS(db.Model):
    id_bitacora = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer)
    nombre_usuario = db.Column(db.String(255))
    accion_realizada = db.Column(db.Text)
    detalles_accion = db.Column(db.Text)
    fecha_acceso = db.Column(db.DateTime)
    ip_acceso = db.Column(db.String(50))

class BITACORA_SESION(db.Model):
    id_sesion = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer)
    nombre_usuario = db.Column(db.String(255))
    correo_usuario = db.Column(db.String(255))
    fecha_inicio = db.Column(db.DateTime)
    ip_usuario = db.Column(db.String(50))
    url_solicitada = db.Column(db.String(255))

class TBL_HORARIOS_ESCOLARES(db.Model):
    id_horario = db.Column(db.Integer, primary_key=True)
    id_asignatura = db.Column(db.Integer, db.ForeignKey('tbl_asignaturas.id_asignatura'), nullable=False)
    id_docente = db.Column(db.Integer, db.ForeignKey('tbl_docentes.id_docentes'), nullable=False)
    id_grado = db.Column(db.Integer, db.ForeignKey('tbl_grados.id_grado'), nullable=False)
    id_grupo = db.Column(db.Integer, db.ForeignKey('tbl_grupos.id_grupos'), nullable=False)
    id_carrera_tecnica = db.Column(db.Integer, db.ForeignKey('tbl_carreras_tecnicas.id_carrera_tecnica'), nullable=False)
    ciclo_escolar = db.Column(db.String(10), nullable=False)
    dias_horarios = db.Column(db.Text)

class TBL_HORARIO_ALUMNOS(db.Model):
    id_horario_alumno = db.Column(db.Integer, primary_key=True)
    id_horario = db.Column(db.Integer, db.ForeignKey('tbl_horarios_escolares.id_horario'), nullable=False)
    id_alumno = db.Column(db.Integer, db.ForeignKey('tbl_alumnos.id_alumnos'), nullable=False)
    fecha_inscripcion = db.Column(db.DateTime, default=db.func.current_timestamp())

class TBL_ASISTENCIAS(db.Model):
    id_asistencia = db.Column(db.Integer, primary_key=True)
    id_alumno = db.Column(db.Integer, db.ForeignKey('tbl_alumnos.id_alumnos'), nullable=False)
    id_horario = db.Column(db.Integer, db.ForeignKey('tbl_horarios_escolares.id_horario'), nullable=False)
    fecha = db.Column(db.DateTime, nullable=False)
    estado_asistencia = db.Column(db.String(50), nullable=False)
    comentarios = db.Column(db.Text)

class TBL_ACTIVIDADES_NOTICIAS(db.Model):
    id_actividades_noticias = db.Column(db.Integer, primary_key=True)
    imagen_actividad_noticia = db.Column(db.LargeBinary, nullable=False)
    titulo_actividad_noticia = db.Column(db.String(20), nullable=False)
    descripcion_actividad_noticia = db.Column(db.Text, nullable=False)
    fecha_actividad_noticias = db.Column(db.DateTime)

class TBL_INFO_INSCRIPTION(db.Model):
    id_info_inscription = db.Column(db.Integer, primary_key=True)
    txt_info_inscription = db.Column(db.Text)
    requeriments_info_inscription = db.Column(db.Text)
    periodo_info_inscripcion = db.Column(db.Text)
    imagen_info_inscription = db.Column(db.LargeBinary)

class TBL_ACTIVIDADES_CULTURALES(db.Model):
    id_actividad_cultural = db.Column(db.Integer, primary_key=True)
    imagen_actividad_cultural = db.Column(db.LargeBinary)
    nombre_actividad_cultural = db.Column(db.Text)
    descripcion_actividad_cultural = db.Column(db.Text)

class TBL_SOBRE_NOSOTROS(db.Model):
    id_sobre_nosotros = db.Column(db.Integer, primary_key=True)
    txt_sobre_nosotros = db.Column(db.Text)
    imagen_sobre_nosotros = db.Column(db.LargeBinary)
    fecha_sobre_nosotros = db.Column(db.DateTime)

class TBL_INFO_BECAS(db.Model):
    id_info_becas = db.Column(db.Integer,primary_key=True)
    titulo_info_becas = db.Column(db.String(20))
    descripcion_info_becas = db.Column(db.Text)
    requisitos_info_becas = db.Column(db.Text)
    foto_info_becas = db.Column(db.LargeBinary)

class TBL_NOTIFICACIONES(db.Model):
    id_notificaciones = db.Column(db.Integer, primary_key=True)
    alumno_id = db.Column(db.Integer, db.ForeignKey('tbl_alumnos.id_alumnos'), nullable=False)
    subject_notificacion = db.Column(db.Text)
    message_notificacion = db.Column(db.Text)
    fecha_notificaciones = db.Column(db.DateTime, default=datetime.utcnow)

class TBL_NOTIFICACIONES_DOCENTES(db.Model):
    id_notificaciones_docentes = db.Column(db.Integer, primary_key=True)
    docente_id = db.Column(db.Integer, db.ForeignKey('tbl_docentes.id_docentes'), nullable=False)
    subject_notificacion_doc = db.Column(db.Text)
    message_notificacion_doc = db.Column(db.Text)
    fecha_notificaciones_doc = db.Column(db.DateTime, default=datetime.utcnow)


class TBL_ALUMNOS_AGREGADOS(db.Model):
    id_alumnos_agregados = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('tbl_usuarios.id_usuario'), nullable=False)
    id_alumno = db.Column(db.Integer, db.ForeignKey('tbl_alumnos.id_alumnos'), nullable=False)


class TBL_SOLICITANTES(db.Model):
    id_solicitante = db.Column(db.Integer, primary_key=True)
    ficha_no = db.Column(db.String(50), nullable=False)
    apellido_paterno = db.Column(db.String(100), nullable=False)
    apellido_materno = db.Column(db.String(100), nullable=False)
    nombres = db.Column(db.String(100), nullable=False)
    foto = db.Column(db.LargeBinary)
    direccion = db.Column(db.String(250), nullable=False)
    localidad = db.Column(db.String(100), nullable=False)
    municipio = db.Column(db.String(100), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    promedio_sec = db.Column(db.Numeric(3, 2), nullable=False)
    fecha_nacimiento = db.Column(db.DateTime, nullable=False)
    beca = db.Column(db.Boolean, nullable=False)
    tipo_discapacidad = db.Column(db.String(100))
    hablante_lengua_indigena = db.Column(db.Boolean, nullable=False)
    correo_electronico = db.Column(db.String(100), nullable=False)
    escuela_procedencia = db.Column(db.String(100), nullable=False)
    cct = db.Column(db.String(50))
    tipo_secundaria = db.Column(db.String(50))
    direccion_secundaria = db.Column(db.String(250))
    localidad_secundaria = db.Column(db.String(100))
    municipio_secundaria = db.Column(db.String(100))
    estado_secundaria = db.Column(db.String(100))
    nombre_padre_tutor = db.Column(db.String(100), nullable=False)
    id_relacion_familiar = db.Column(db.Integer, db.ForeignKey('tbl_relacion_familiar.id_relacion_familiar'))
    telefono_alumno = db.Column(db.BigInteger)
    telefono_tutor = db.Column(db.BigInteger)
    telefono_familiar = db.Column(db.BigInteger)
    id_carrera_tecnica = db.Column(db.Integer, db.ForeignKey('tbl_carreras_tecnicas.id_carrera_tecnica'))
    id_info_becas = db.Column(db.Integer, db.ForeignKey('tbl_info_becas.id_info_becas'))
    fecha_registro = db.Column(db.DateTime, default=db.func.current_timestamp())


class TBL_REGISTRO_ACCESO_DOCENTE(db.Model):
    id_registro = db.Column(db.Integer, primary_key=True)
    id_docente = db.Column(db.Integer, db.ForeignKey('tbl_docentes.id_docentes'), nullable=False)
    nombre_docente = db.Column(db.String(255), nullable=False)
    fecha_registro_acceso = db.Column(db.DateTime, nullable=False)
    codigo_qr = db.Column(db.String(255), nullable=True)
    

class TBL_REGISTRO_ACCESO_ALUMNO(db.Model):
    id_registro_alumno = db.Column(db.Integer, primary_key=True)
    id_alumnox = db.Column(db.Integer, db.ForeignKey('tbl_alumnos.id_alumnos'), nullable=False)
    nombre_alumnox = db.Column(db.String(255), nullable=False)
    fecha_registro_acceso_alumno = db.Column(db.DateTime, nullable=False)
    codigo_qr_alumno = db.Column(db.String(255), nullable=True)