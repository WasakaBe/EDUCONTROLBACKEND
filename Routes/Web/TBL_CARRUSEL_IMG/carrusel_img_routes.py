from flask import Blueprint, jsonify, request
from Database.Database import db, TBL_CARRUSEL_IMG
from sqlalchemy.exc import SQLAlchemyError
from base64 import b64encode

carrusel_img_bp = Blueprint('carrusel_img_bp', __name__)

@carrusel_img_bp.route('/carrusel_imgs', methods=['GET'])
def get_all_carrusel_imgs():
    try:
        carrusel_imgs = TBL_CARRUSEL_IMG.query.all()
        result = [{'id_carrusel': img.id_carrusel,
                   'carrusel': b64encode(img.carrusel).decode('utf-8') if img.carrusel else None
                   } for img in carrusel_imgs]
        return jsonify({'carrusel_imgs': result})
    except Exception as e:
        print(f'Error al obtener las imágenes del carrusel: {str(e)}')
        return jsonify({'message': 'Error al obtener las imágenes del carrusel', 'error': str(e)}), 500

@carrusel_img_bp.route('/carrusel_imgs/delete/<int:id>', methods=['DELETE'])
def delete_carrusel_img(id):
    carrusel_img = TBL_CARRUSEL_IMG.query.get(id)
    if not carrusel_img:
        return jsonify({'message': 'Imagen del carrusel no encontrada'}), 404

    try:
        db.session.delete(carrusel_img)
        db.session.commit()
        return jsonify({'message': 'Imagen del carrusel eliminada exitosamente'})
    except Exception as e:
        print(f'Error al eliminar la imagen del carrusel: {str(e)}')
        return jsonify({'message': 'Error al eliminar la imagen del carrusel', 'error': str(e)}), 500

@carrusel_img_bp.route('/carrusel_imgs/insert', methods=['POST'])
def insert_carrusel_img():
    try:
        img_file = request.files.get('carrusel')
        if not img_file:
            return jsonify({'message': 'No se proporcionó una imagen para insertar'}), 400

        nueva_img = TBL_CARRUSEL_IMG(
            carrusel=img_file.read()
        )
        db.session.add(nueva_img)
        db.session.commit()
        return jsonify({'message': 'Imagen del carrusel insertada exitosamente'}), 201
    except Exception as e:
        print(f'Error al insertar la imagen del carrusel: {str(e)}')
        return jsonify({'message': 'Error al insertar la imagen del carrusel', 'error': str(e)}), 500
