from flask import (
    Blueprint,
    redirect
)
from app.api.utils import response

available_nns_response = [{
    'name': 'monodepth',
    'ext_link': 'https://github.com/mrharicot/monodepth'
}]

root_api_v1 = Blueprint(name='root_api_v1', import_name=__name__, url_prefix="/v1")

@root_api_v1.errorhandler(400)
def page_not_found(e):
    return response(400, {'message':'Bad Request error'})

@root_api_v1.route('/',methods=['GET'])
def root():
    return redirect('/v1/cnns')

@root_api_v1.route('/cnns',methods=['GET'])
def available_nns():
    return response(200, available_nns_response)