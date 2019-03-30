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

AVAILABLE_MODELS = ['kitti','eigen','cityscapes']

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

monodepth_api_v1 = Blueprint(name='monodepth_api_v1', import_name=__name__, url_prefix="/api/v1.0/nns/monodepth")

@monodepth_api_v1.route('/')
def root():
    return response(200, AVAILABLE_MODELS)

@monodepth_api_v1.errorhandler(400)
def page_not_found(e):
    return response(400, {'message':'Bad Request error'})

@monodepth_api_v1.route('/<model>', methods=['POST'])
def process_image(model):
    if model not in AVAILABLE_MODELS:
        return response(404, {'message':'Model not found'})
    if 'image' not in request.files:
        return response(400, {'message':'No image part'})
    image = request.files['image']
    if image.filename == '':
        return response(400, {'message':'No selected image'})
    if image and allowed_extension(image.filename):
        filename = secure_filename(image.filename)
        
        input_image = misc.imread(BytesIO(image.read()))
        input_image = misc.imresize(input_image, [100, 100], interp='lanczos')
        
        im = Image.fromarray(input_image)
        
        imgByteArr = BytesIO()
        im.save(imgByteArr, format='JPEG')
        imgByteArr.seek(0)
        
        return send_file(imgByteArr, mimetype='image/jpeg',as_attachment=True, attachment_filename=filename)

def allowed_extension(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def brightImage(data):
    im = PIL.Image.fromarray(data)
    enhancer = ImageEnhance.Brightness(im)
    enhanced_im = enhancer.enhance(2.8)
    imgByteArr = BytesIO()
    enhanced_im.save(imgByteArr, format='JPG')
    imgByteArr = imgByteArr.getvalue()
    return imgByteArr