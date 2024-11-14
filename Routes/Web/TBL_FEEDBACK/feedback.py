from base64 import b64encode
from flask import Flask
from Database.Database import TBL_USUARIOS, db, TBL_FEEDBACK  # Importamos la clase del modelo
from sqlalchemy.exc import SQLAlchemyError
from flask import Blueprint, jsonify, request
feedback_bp = Blueprint('feedback_bp', __name__)

# Ruta para crear un feedback
# Ruta para crear un feedback
@feedback_bp.route('/create/feedback', methods=['POST'])
def create_feedback():
    try:
        data = request.json
        idusuario = data.get('idusuario')
        emocion_feedback = data.get('emocion_feedback')

        # Validar que los datos obligatorios estén presentes
        if not idusuario or not emocion_feedback:
            return jsonify({'error': 'Faltan datos obligatorios'}), 400

        # Crear nuevo feedback solo con idusuario y emocion_feedback
        new_feedback = TBL_FEEDBACK(
            idusuario=idusuario,
            emocion_feedback=emocion_feedback
        )

        db.session.add(new_feedback)
        db.session.commit()

        return jsonify({'message': 'Feedback creado con éxito', 'id': new_feedback.id_feedback}), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Ha ocurrido un error al intentar crear el feedback'}), 500


# Ruta para obtener todos los feedbacks con información del usuario
@feedback_bp.route('/view/feedbacks', methods=['GET'])
def get_feedbacks():
    try:
        # Realizamos la consulta uniendo la tabla de feedback con la de usuarios
        feedbacks = db.session.query(
            TBL_FEEDBACK,
            TBL_USUARIOS.nombre_usuario,
            TBL_USUARIOS.correo_usuario,
            TBL_USUARIOS.foto_usuario
        )\
        .join(TBL_USUARIOS, TBL_FEEDBACK.idusuario == TBL_USUARIOS.id_usuario)\
        .all()

        result = []
        for feedback in feedbacks:
            feedback_data = feedback[0]  # Los datos del feedback están en la primera posición
            nombre_usuario = feedback[1]  # Nombre del usuario
            correo_usuario = feedback[2]  # Correo del usuario
            foto_usuario = feedback[3]    # Foto del usuario

            # Construimos el resultado con todos los detalles
            result.append({
                'id_feedback': feedback_data.id_feedback,
                'idusuario': feedback_data.idusuario,
                'nombre_usuario': nombre_usuario,
                'correo_usuario': correo_usuario,
                'foto_usuario': b64encode(foto_usuario).decode('utf-8') if foto_usuario else None,
                'emocion_feedback': feedback_data.emocion_feedback,
                'motivo_feedback': feedback_data.motivo_feedback
            })

        return jsonify(result), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# Ruta para obtener un feedback específico por ID
@feedback_bp.route('/id/feedback/<int:id>', methods=['GET'])
def get_feedback_by_id(id):
    try:
        feedback = TBL_FEEDBACK.query.get(id)
        if not feedback:
            return jsonify({'error': 'Feedback no encontrado'}), 404

        result = {
            'id_feedback': feedback.id_feedback,
            'idusuario': feedback.idusuario,
            'emocion_feedback': feedback.emocion_feedback,
            'motivo_feedback': feedback.motivo_feedback
        }
        return jsonify(result), 200
    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 500

# Ruta para eliminar un feedback por ID
@feedback_bp.route('/delete/feedback/<int:id>', methods=['DELETE'])
def delete_feedback(id):
    try:
        feedback = TBL_FEEDBACK.query.get(id)
        if not feedback:
            return jsonify({'error': 'Feedback no encontrado'}), 404

        db.session.delete(feedback)
        db.session.commit()
        return jsonify({'message': 'Feedback eliminado con éxito'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


