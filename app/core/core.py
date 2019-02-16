from flask import (
    Flask,
    render_template,
    request,
    flash
    )
from time import sleep
import threading


def create_app():
    app = Flask('app')
    app.config.update()
    app.config.timezone = 'UTC'

    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/scanning', methods=['GET', 'POST'])
    def scanning():
        return render_template('scanning.html')


    @app.route('/slow_http', methods=['GET', 'POST'])
    def slow_http():
        from utils.slow_http import start_slow_http_attack, check_if_url_is_valid, stop_slow_http_attack
        if request.method == 'GET':
            return render_template('slow_http.html')
        else:
            try:
                url_ = request.form['url_']
            except:
                return render_template('slow_http.html', form=request.form)
            try:
                port = int(request.form['port'])
            except:
                port = 80
            _url_to_check = url_
            if port != 80:
                if _url_to_check.endswith("/"):
                    _url_to_check = _url_to_check[:-1]
                _url_to_check = "%s:%s" % (_url_to_check, port)
            if "http" not in _url_to_check:
                _url_to_check = "http://%s" % _url_to_check
            if not check_if_url_is_valid(_url_to_check):
                return render_template('slow_http.html', form=request.form, errors="Neispravan URL")
            try:
                workers_ = int(request.form['workers'])
            except:
                workers_ = 1000
            try:
                sleep_ = int(request.form['sleep'])
            except:
                sleep_ = 3
            try:
                last_ = int(request.form['attack'])
                if last_ > 120:
                    last_ = 30
            except:
                last_ = 30


            try:
                t = threading.Thread(target=start_slow_http_attack, args=[url_, port, workers_, sleep_])
                t.start()
                sleep(last_)
                t.exit()
            except ConnectionRefusedError as e:
                print("Connection refused")
            except Exception as e:
                pass

            return render_template('slow_http.html')

    return app