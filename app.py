from flask import Flask

def create_app():
    """Create and configure instance of the Flask application"""
    app = Flask(__name__)


    @app.route('/')
    def barebones():
        return 'the crawler'

    return app