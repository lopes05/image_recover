import sys
from image import *
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import requests

import logging

logging.basicConfig(filename='backend.log', level=logging.DEBUG)
logger = logging.getLogger('backend')

UPLOAD_FOLDER = '/tmp/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def hello():
    return "Hello World from Flask!"
import cv2

from flask import Response
import json as js

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

from flask import json
@app.route('/image', methods=['POST'])
def image_url():
    try:
        image = request.files['imgurl']  # get the image URL
        
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        logger.info(image.filename)
        hists = run_process(f'/tmp/{filename}')
        
        logger.info('finished')
        from collections import OrderedDict
        response = app.response_class(
            response=js.dumps(hists),
            status=200,
            mimetype='application/json'
        )
        return response


    except Exception as e:
        logger.error(str(e))
        return 'error'

@app.route('/refilter', methods=['POST'])
def refilter():
    try:
        dados = request.get_json()
        hists = refilter_imgs(dados)
        response = app.response_class(
            response=js.dumps(hists),
            status=200,
            mimetype='application/json'
        )
        return response
    except Exception as e:
        logger.error(str(e))
        return 'error'

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)
