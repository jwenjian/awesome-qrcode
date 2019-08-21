import os
import uuid

from flask import request, jsonify, render_template

from app import app
from app.generator import Generator


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/qrcode/normal', methods=['POST'])
def normal_qrcode():
    text = request.json.get('text')
    try:
        result_base64 = Generator.gen_normal_qrcode(text)
    except Exception as e:
        return jsonify({
            "code": 1,
            "message": e
        })
    return jsonify({
        "code": 0,
        "url": result_base64
    })


@app.route('/qrcode/picture', methods=['POST'])
def picture_qrcode():
    picture_file = request.files['file']
    text = request.form['text']
    temp_file_name = str(uuid.uuid1()) + '.' + picture_file.filename.split('.')[-1:][0].replace('jpeg', 'jpg')
    temp_file_path = os.path.join(os.getcwd(), temp_file_name)
    picture_file.save(temp_file_path)

    try:
        result_base64 = Generator.gen_picture_qrcode(text, temp_file_path)
    except Exception as e:
        return jsonify({
            "code": 1,
            "message": e
        })

    return jsonify({
        "code": 0,
        "url": result_base64
    })


@app.route('/qrcode/gif', methods=['POST'])
def gif_qrcode():
    picture_file = request.files['file']
    text = request.form['text']
    temp_file_name = str(uuid.uuid4()) + '.' + picture_file.filename.split('.')[-1:][0]
    temp_file_path = os.path.join(os.getcwd(), temp_file_name)
    picture_file.save(temp_file_path)

    try:
        result_base64 = Generator.gen_gif_qrcode(text, temp_file_path)
    except Exception as e:
        return jsonify({
            "code": 1,
            "message": e
        })

    return jsonify({
        "code": 0,
        "url": result_base64
    })
