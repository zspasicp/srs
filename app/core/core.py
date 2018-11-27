from flask import (
    Flask,
    render_template
    )


def create_app():
    app = Flask('app')
    app.config.update()
    app.config.timezone = 'UTC'

    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/slow_http')
    def slow_http():
        return render_template('slow_http.html')

    return app