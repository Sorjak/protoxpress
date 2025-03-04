import os

from flask import Flask, request

def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    @app.get('/debug')
    def debug():
        return 'Hello, World!'
    
    @app.post('/scene')
    def post_set_scene():
        scene = request.json.get('scene')
        if not scene:
            return {'success': False}

        return {'success': True, 'msg': f"set scene {scene}"}

    return app