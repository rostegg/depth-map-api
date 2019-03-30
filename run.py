import os
from flask import redirect
from app import create_app
from app.api.monodepth import monodepth_api_v1
from app.api.api_v1 import root_api_v1
from waitress import serve

app = create_app(os.getenv('FLASK_CONFIG_TYPE') or 'dev')
app.register_blueprint(monodepth_api_v1)
app.register_blueprint(root_api_v1)

@app.route('/')
def root():
    return redirect('/api/v1.0')

if __name__ == '__main__':
    host = os.environ.get('IP', '0.0.0.0')
    port = int(os.environ.get("PORT", 5000))
    serve(app, host=host, port=port) if (os.getenv('FLASK_CONFIG_TYPE') == 'prod') else app.run(host=host, port=port)