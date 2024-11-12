import os
import logging
from flask import Flask, jsonify, request,send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from waitress import serve
from dotenv import load_dotenv
from Database.Database import db , PushSubscription
from pywebpush import webpush, WebPushException
import pyodbc


# Importa y registra los blueprints después de inicializar db
from Routes.Web.TBL_TIPO_ROL.tipo_rol_routes import tipo_rol_bp
from Routes.Web.TBL_SEXOS.sexos_routes import sexos_bp
from Routes.Web.TBL_ACTIVOS_CUENTAS.activos_cuentas_routes import activos_cuentas_bp
from Routes.Web.TBL_TRASLADOS.traslados_routes import traslados_bp
from Routes.Web.TBL_TRASLADO_TRANSPORTE.traslado_transporte_routes import traslado_transporte_bp
from Routes.Web.TBL_ASIGNATURAS.asignaturas_routes import asignaturas_bp
from Routes.Web.TBL_GRADOS.grados_routes import grados_bp
from Routes.Web.TBL_GRUPOS.grupos_routes import grupos_bp
from Routes.Web.TBL_PREGUNTAS.preguntas_routes import preguntas_bp
from Routes.Web.TBL_CARRERAS_TECNICAS.carreras_tecnicas_routes import carreras_tecnicas_bp
from Routes.Web.TBL_CLINICAS.clinicas_routes import clinicas_bp
from Routes.Web.TBL_PAISES.paises_routes import paises_bp
from Routes.Web.TBL_ESTADOS.estados_routes import estados_bp
from Routes.Web.TBL_RELACION_FAMILIAR.relacion_familiar_routes import relacion_familiar_bp
from Routes.Web.TBL_MOTIVO_CREDENCIAL.motivo_credencial_routes import motivo_credencial_bp
from Routes.Web.TBL_CARRUSEL_IMG.carrusel_img_routes import carrusel_img_bp
from Routes.Web.TBL_MENSAJES_CONTACTOS.mensajes_contactos_routes import mensajes_contactos_bp
from Routes.Web.TBL_USUARIOS.usuarios_routes import usuarios_bp
from Routes.Web.TBL_DOCENTES.docentes_routes import docentes_bp
from Routes.Web.TBL_ALUMNOS.alumnos_routes import alumnos_bp
from Routes.Web.TBL_MENSAJES_MOTIVO_CREDENCIAL.mensajes_motivo_credencial_routes import mensajes_motivo_credencial_bp
from Routes.Web.TBL_CREDENCIALES_ESCOLARES.credenciales_escolares_routes import credenciales_escolares_bp
from Routes.Web.TBL_WELCOME.welcome_routes import welcome_bp
from Routes.Web.TBL_MISION.mision_routes import mision_bp
from Routes.Web.TBL_VISION.vision_routes import vision_bp
from Routes.Web.TBL_HORARIOS_ESCOLARES.horarios_escolares_routes import horarios_escolares_bp
from Routes.Web.TBL_HORARIO_ALUMNOS.horario_alumnos_routes import horario_alumnos_bp
from Routes.Web.TBL_ASISTENCIAS.asistencias_routes import asistencias_bp
from Routes.Web.TBL_ACTIVIDADES_NOTICIAS.actividades_noticias_routes import actividades_noticias_bp
from Routes.Web.TBL_INFO_INSCRIPTION.info_inscription_routes import info_inscription_bp
from Routes.Web.TBL_ACTIVIDADES_CULTURALES.actividades_culturales_routes import actividades_culturales_bp
from Routes.Web.TBL_SOBRE_NOSOTROS.sobre_nosotros_routes import sobre_nosotros_bp
from Routes.Web.TBL_INFO_BECAS.info_becas_routes import info_becas_bp
from Routes.Web.TBL_NOTIFICACIONES.notifications_bp import notifications_bp
from Routes.Web.TBL_NOTIFICACIONES_DOCENTES.notificaciones_docentes_bp import notificaciones_docentes_bp
from Routes.Web.TBL_SOLICITANTES.solicitantes_routes import solicitantes_bp
from Routes.Web.TBL_REGISTRO_ACCESO_DOCENTE.registro_acceso_bp import registro_acceso_bp
from Routes.Web.TBL_REGISTRO_ACCESO_ALUMNO.registro_acceso_alumno_bp import registro_acceso_alumnos_bp
from Routes.Web.TBL_FEEDBACK.feedback import feedback_bp
#?: LOGIN - REGISTRO - RECUPERACION - FORMULARIOS
from Routes.Auth.AuthLogin.auth_routes import auth_bp
from Routes.Auth.AuthRegister.register_routes import register_bp
from Routes.Auth.AuthForgout.password_reset_routes import password_reset_bp
#?: WEAR
from Routes.Wear.wear  import wear_bp

# Cargar las variables de entorno
load_dotenv()

VAPID_PUBLIC_KEY = os.getenv("VAPID_PUBLIC_KEY")
VAPID_PRIVATE_KEY = os.getenv("VAPID_PRIVATE_KEY")
VAPID_CLAIMS = {
    "sub": "mailto:mtzalan080@gmail.com"
}

# Configuración de logging
logging.getLogger('waitress.queue').setLevel(logging.ERROR)

# Inicializar la aplicación Flask
app = Flask(__name__)
# Configuración de CORS
CORS(app, supports_credentials=True)


# Configuración de SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads/'

db.init_app(app)

# Manejo de errores
@app.errorhandler(Exception)
def handle_error(e):
    if isinstance(e, SQLAlchemyError):
        return jsonify({'error': 'Error de la base de datos'}), 500
    return jsonify({'error': str(e)}), 500


try:
    connection = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=educontrolservidor.database.windows.net;'
        'DATABASE=EDUCBTAOFICIAL;'
        'UID=adminsql;'
        'PWD=Telcel4773;'
        'Encrypt=yes;'
        'TrustServerCertificate=no;'
        'Connection Timeout=30;'
    )
    print("Conexión exitosa a la base de datos.")
    connection.close()
except pyodbc.Error as e:
    print("Error al conectar a la base de datos:", e)
    
# Ruta principal
@app.route('/')
def hello_world():
    return 'API BACKEND CBTA 5 OFICIAL'

# Ruta para descargar el archivo CSV de ejemplo
@app.route('/api/example_csv')
def download_example_csv():
    try:
        return send_from_directory(
            directory=os.path.join(app.root_path, 'static'),
            path='ejemplo.csv',
            as_attachment=True
        )
    except FileNotFoundError:
        return jsonify({'error': 'Archivo no encontrado'}), 404
    
# Ruta para descargar el archivo CSV de ejemplo
@app.route('/api/example_docent_csv')
def download_example_docent_csv():
    try:
        return send_from_directory(
            directory=os.path.join(app.root_path, 'static'),
            path='ejemplo_docente.csv',
            as_attachment=True
        )
    except FileNotFoundError:
        return jsonify({'error': 'Archivo no encontrado'}), 404

@app.route('/api/subscribe', methods=['POST'])
def subscribe():
    data = request.get_json()
    try:
        # Extraer los datos de la suscripción desde la solicitud
        endpoint = data.get("endpoint")
        keys = data.get("keys", {})
        keys_p256dh = keys.get("p256dh")
        keys_auth = keys.get("auth")

        # Verificar que todos los datos necesarios estén presentes
        if not endpoint or not keys_p256dh or not keys_auth:
            return jsonify({"error": "Datos de suscripción incompletos."}), 400

        # Crear una nueva entrada de suscripción
        new_subscription = PushSubscription(endpoint=endpoint, keys_p256dh=keys_p256dh, keys_auth=keys_auth)
        db.session.add(new_subscription)
        db.session.commit()

        return jsonify({"message": "Suscripción almacenada con éxito"}), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Error de la base de datos"}), 500
    except Exception as e:
        return jsonify({"error": f"Error inesperado: {str(e)}"}), 500


@app.route('/api/notify', methods=['POST'])
def notify():
    try:
        # Aquí asumimos que el payload (el mensaje a enviar) viene en el cuerpo de la solicitud
        data = request.get_json()
        message = data.get("message", "¡Tienes una nueva notificación!")

        # Recuperar todas las suscripciones de la base de datos
        subscriptions = PushSubscription.query.all()

        # Iterar sobre cada suscripción y enviar la notificación
        for sub in subscriptions:
            subscription_info = {
                "endpoint": sub.endpoint,
                "keys": {
                    "p256dh": sub.keys_p256dh,
                    "auth": sub.keys_auth
                }
            }
            try:
                # Enviar la notificación a cada suscriptor
                webpush(
                    subscription_info,
                    message,
                    vapid_private_key=VAPID_PRIVATE_KEY,
                    vapid_claims=VAPID_CLAIMS
                )
                print(f"Notificación enviada a {sub.endpoint}")
            except WebPushException as ex:
                print(f"Error al enviar la notificación: {ex}")

        return jsonify({"message": "Notificaciones enviadas"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


app.register_blueprint(tipo_rol_bp, url_prefix='/api')
app.register_blueprint(sexos_bp, url_prefix='/api')
app.register_blueprint(activos_cuentas_bp, url_prefix='/api')
app.register_blueprint(traslados_bp, url_prefix='/api')
app.register_blueprint(traslado_transporte_bp, url_prefix='/api')
app.register_blueprint(asignaturas_bp, url_prefix='/api')
app.register_blueprint(grados_bp, url_prefix='/api')
app.register_blueprint(grupos_bp, url_prefix='/api')
app.register_blueprint(preguntas_bp, url_prefix='/api')
app.register_blueprint(carreras_tecnicas_bp, url_prefix='/api')
app.register_blueprint(clinicas_bp, url_prefix='/api')
app.register_blueprint(paises_bp, url_prefix='/api')
app.register_blueprint(estados_bp, url_prefix='/api')
app.register_blueprint(relacion_familiar_bp, url_prefix='/api')
app.register_blueprint(motivo_credencial_bp, url_prefix='/api')
app.register_blueprint(carrusel_img_bp, url_prefix='/api')
app.register_blueprint(mensajes_contactos_bp, url_prefix='/api')
app.register_blueprint(usuarios_bp, url_prefix='/api')
app.register_blueprint(docentes_bp, url_prefix='/api')
app.register_blueprint(alumnos_bp, url_prefix='/api')
app.register_blueprint(mensajes_motivo_credencial_bp, url_prefix='/api')
app.register_blueprint(welcome_bp, url_prefix='/api')
app.register_blueprint(mision_bp, url_prefix='/api')
app.register_blueprint(vision_bp, url_prefix='/api')
app.register_blueprint(horarios_escolares_bp, url_prefix='/api')
app.register_blueprint(horario_alumnos_bp, url_prefix='/api')
app.register_blueprint(asistencias_bp, url_prefix='/api')
app.register_blueprint(actividades_noticias_bp, url_prefix='/api')
app.register_blueprint(info_inscription_bp, url_prefix='/api')
app.register_blueprint(actividades_culturales_bp, url_prefix='/api')
app.register_blueprint(sobre_nosotros_bp, url_prefix='/api')
app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(register_bp, url_prefix='/api')
app.register_blueprint(password_reset_bp, url_prefix='/api')
app.register_blueprint(credenciales_escolares_bp, url_prefix='/api')
app.register_blueprint(info_becas_bp,url_prefix='/api')
app.register_blueprint(notifications_bp,url_prefix='/api')
app.register_blueprint(notificaciones_docentes_bp,url_prefix='/api')
app.register_blueprint(registro_acceso_bp,url_prefix='/api')
app.register_blueprint(registro_acceso_alumnos_bp, url_prefix='/api')
app.register_blueprint(solicitantes_bp,url_prefix='/api')
app.register_blueprint(feedback_bp,url_prefix='/api')

app.register_blueprint(wear_bp)
if __name__ == '__main__':
    serve(app, host='127.0.0.1', port=50023)
