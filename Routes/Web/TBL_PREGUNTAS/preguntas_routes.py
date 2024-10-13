from flask import Blueprint, jsonify, request
from Database.Database import db, TBL_PREGUNTAS
from sqlalchemy.exc import SQLAlchemyError

preguntas_bp = Blueprint('preguntas_bp', __name__)

# Ruta para insertar una nueva pregunta
@preguntas_bp.route('/pregunta/insert', methods=['POST'])
def create_pregunta():
    data = request.get_json()
    nombre_preguntas = data.get('nombre_preguntas')
    
    if not nombre_preguntas:
        return jsonify({'error': 'El nombre de la pregunta es obligatorio'}), 400

    new_pregunta = TBL_PREGUNTAS(nombre_preguntas=nombre_preguntas)
    
    try:
        db.session.add(new_pregunta)
        db.session.commit()
        return jsonify({'message': 'Pregunta creada exitosamente'}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Ruta para visualizar todas las preguntas
@preguntas_bp.route('/pregunta', methods=['GET'])
def get_all_preguntas():
    preguntas = TBL_PREGUNTAS.query.all()
    result = [{'id_preguntas': pregunta.id_preguntas, 'nombre_preguntas': pregunta.nombre_preguntas} for pregunta in preguntas]
    return jsonify(result), 200

# Ruta para visualizar una pregunta por su ID
@preguntas_bp.route('/pregunta/<int:id>', methods=['GET'])
def get_pregunta(id):
    pregunta = TBL_PREGUNTAS.query.get(id)
    if not pregunta:
        return jsonify({'error': 'Pregunta no encontrada'}), 404
    return jsonify({'id_preguntas': pregunta.id_preguntas, 'nombre_preguntas': pregunta.nombre_preguntas}), 200

# Ruta para actualizar una pregunta por su ID
@preguntas_bp.route('/pregunta/<int:id>', methods=['PUT'])
def update_pregunta(id):
    data = request.get_json()
    pregunta = TBL_PREGUNTAS.query.get(id)
    
    if not pregunta:
        return jsonify({'error': 'Pregunta no encontrada'}), 404

    nombre_preguntas = data.get('nombre_preguntas')
    if not nombre_preguntas:
        return jsonify({'error': 'El nombre de la pregunta es obligatorio'}), 400

    pregunta.nombre_preguntas = nombre_preguntas

    try:
        db.session.commit()
        return jsonify({'message': 'Pregunta actualizada exitosamente'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Ruta para eliminar una pregunta por su ID
@preguntas_bp.route('/pregunta/<int:id>', methods=['DELETE'])
def delete_pregunta(id):
    pregunta = TBL_PREGUNTAS.query.get(id)
    if not pregunta:
        return jsonify({'error': 'Pregunta no encontrada'}), 404

    try:
        db.session.delete(pregunta)
        db.session.commit()
        return jsonify({'message': 'Pregunta eliminada exitosamente'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
