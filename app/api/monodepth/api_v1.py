import os
from flask import (
    Blueprint,
    request,
    send_file
)
from io import BytesIO, StringIO
from app.api.utils import response
from werkzeug.utils import secure_filename
from PIL import Image, ImageEnhance
import numpy as np
import PIL
from scipy import misc
from app.cnns.monodepth.monodepth_bridge import MonodepthBridge as mb
from app.api.cache import cache

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

monodepth_api_v1 = Blueprint(name='monodepth_api_v1', import_name=__name__, url_prefix="/v1/cnns/monodepth")

@monodepth_api_v1.route('/')
def root():
    return response(200, mb.AVAILABLE_MODELS)

@monodepth_api_v1.errorhandler(400)
def page_not_found(e):
    return response(400, {'message':'Bad Request error'})

@monodepth_api_v1.route('/<model>', methods=['POST'])
@cache.cached(timeout=60)
def process_image(model):
    if model not in mb.AVAILABLE_MODELS:
        return response(404, {'message':'Model not found'})
    if 'image' not in request.files:
        return response(400, {'message':'No image part'})
    image = request.files['image']
    if image.filename == '':
        return response(400, {'message':'No selected image'})
    if image and allowed_extension(image.filename):
        filename = secure_filename(image.filename)
        #temporary error handler
        try:
            img = BytesIO(image.read())
            img.seek(0)
            mono_bridge = mb(img)
            depth_map = mono_bridge.generate_depth_map(model)
        except:
            return response(500, {'message':'unable to process images'})
        
        return send_file(depth_map, mimetype='image/png',as_attachment=True, attachment_filename=filename)

def allowed_extension(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
