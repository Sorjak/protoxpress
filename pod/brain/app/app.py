import os

from flask import Flask, request

from .lib import init_board, set_scene

def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    init_board()

    @app.get('/debug')
    def debug():
        return 'Hello, World!'
    
    @app.post('/scene')
    def post_set_scene():
        scene = request.json.get('scene')
        if not scene:
            return {'success': False, 'error': 'No scene provided'}, 400

        try:
            set_scene(scene)
        except Exception as e:
            return {'success': False, 'error': str(e)}, 400

        return {'success': True, 'msg': f"Set scene {scene}"}

    return app
