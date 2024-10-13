from flask import Blueprint, jsonify, request
from Database.Database import db, TBL_WELCOME
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from base64 import b64encode, b64decode

welcome_bp = Blueprint('welcome_bp', __name__)

# Ruta para insertar una nueva bienvenida
@welcome_bp.route('/welcomes/insert', methods=['POST'])
def create_welcome():
    data = request.form
    welcome_text = data.get('welcome_text')
    foto_welcome = request.files.get('foto_welcome')

    if not welcome_text or not foto_welcome:
        return jsonify({'error': 'El texto de bienvenida y la foto son obligatorios'}), 400

    new_welcome = TBL_WELCOME(
        welcome_text=welcome_text,
        foto_welcome=foto_welcome.read()
    )

    try:
        db.session.add(new_welcome)
        db.session.commit()
        return jsonify({'message': 'Bienvenida creada exitosamente'}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Ruta para visualizar todas las bienvenidas
@welcome_bp.route('/welcome', methods=['GET'])
def get_all_welcomes():
    welcomes = TBL_WELCOME.query.all()
    result = [{
        'id_welcome': welcome.id_welcome,
        'welcome_text': welcome.welcome_text,
        'foto_welcome': b64encode(welcome.foto_welcome).decode('utf-8') if welcome.foto_welcome else None
    } for welcome in welcomes]
    return jsonify(result), 200

# Ruta para visualizar una bienvenida por su ID
@welcome_bp.route('/welcome/<int:id>', methods=['GET'])
def get_welcome(id):
    welcome = TBL_WELCOME.query.get(id)
    if not welcome:
        return jsonify({'error': 'Bienvenida no encontrada'}), 404
    return jsonify({
        'id_welcome': welcome.id_welcome,
        'welcome_text': welcome.welcome_text,
        'foto_welcome': b64encode(welcome.foto_welcome).decode('utf-8') if welcome.foto_welcome else None
    }), 200

# Ruta para actualizar una bienvenida por su ID
@welcome_bp.route('/welcome/update/<int:id>', methods=['PUT'])
def update_welcome(id):
    data = request.form
    welcome = TBL_WELCOME.query.get(id)

    if not welcome:
        return jsonify({'error': 'Bienvenida no encontrada'}), 404

    welcome_text = data.get('welcome_text')
    foto_welcome = request.files.get('foto_welcome')

    if welcome_text:
        welcome.welcome_text = welcome_text
    if foto_welcome:
        welcome.foto_welcome = foto_welcome.read()

    try:
        db.session.commit()
        return jsonify({'message': 'Bienvenida actualizada exitosamente'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Ruta para eliminar una bienvenida por su ID
@welcome_bp.route('/welcome/<int:id>', methods=['DELETE'])
def delete_welcome(id):
    welcome = TBL_WELCOME.query.get(id)
    if not welcome:
        return jsonify({'error': 'Bienvenida no encontrada'}), 404

    try:
        db.session.delete(welcome)
        db.session.commit()
        return jsonify({'message': 'Bienvenida eliminada exitosamente'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    