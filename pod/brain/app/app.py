import os

from flask import Flask, request

from .lib import init_board, set_action

def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    init_board()

    @app.get('/debug')
    def debug():
        return 'Hello, World!'
    
    @app.post('/action')
    def post_set_action():
        action = request.json.get('action')
        if not action:
            return {'success': False, 'error': 'No action provided'}, 400

        try:
            set_action(action)
        except Exception as e:
            return {'success': False, 'error': str(e)}, 400

        return {'success': True, 'msg': f"Set action {action}"}

    return app
