from flask import (
    Flask,
    render_template,
    request
    )


def create_app():
    app = Flask('app')
    app.config.update()
    app.config.timezone = 'UTC'

    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/slow_http', methods=['GET', 'POST'])
    def slow_http():
        from utils.slow_http import start_slow_http_attack
        if request.method == 'GET':
            return render_template('slow_http.html')
        else:
            if "url_" in request.form:
                url_ = request.form['url_']
            else:
                return render_template('slow_http.html')
            port = int(request.form['port'])
            workers_ = int(request.form['workers'])
            sleep_ = int(request.form['sleep'])
            try:
                start_slow_http_attack(url_, port, workers_, sleep_)
            except ConnectionRefusedError as e:
                print("Connection refused")
            except Exception as e:
                pass

            return render_template('slow_http.html')

    return app