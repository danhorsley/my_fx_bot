from flask import Flask, render_template

def create_app():
    """Create and configure instance of the Flask application"""
    app = Flask(__name__)


    @app.route('/')
    def barebones():
        return render_template('base.html')

    return app