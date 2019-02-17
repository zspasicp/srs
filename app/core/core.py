from flask import (
    Flask,
    render_template,
    request,
    flash
    )
from time import sleep
import threading
import os


def create_app():
    app = Flask('app')
    app.config.update()
    app.config.timezone = 'UTC'

    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/scanning', methods=['GET', 'POST'])
    def scanning():
        from utils.network_scan import create_scan_command
        from utils.xml2html import create_html
        import subprocess
        if request.method == 'GET':
            return render_template('scanning.html')
        else:
            url_ = request.form['url_']
            if url_ is None or len(url_) == 0:
                return render_template('scanning.html', errors='Empty URL given')
            option = request.form['option']
            command = None
            if option == 'quick_plus':
                command = create_scan_command(enable_version_detection=True,
                                              enable_OS_detection=True,
                                              target=url_)
                command = command.split()
                command.append('-T4')
                command.append('-F')
                command.append('--version-light')
            elif option == 'ping':
                command = create_scan_command(target=url_)
                command = command.split()
                command.append('-sn')
            elif option == 'quick':
                command = create_scan_command(target=url_)
                command = command.split()
                command.append('-T4')
                command.append('-F')
            else:
                command = create_scan_command(target=url_)
                command = command.split()
            try:
                pass
                proc = subprocess.Popen(command)
                proc.communicate()
            except:
                return render_template('scanning.html', errors='Unable to perform scanning')
            with open(os.path.join('output', url_), 'rb') as f:
                data = f.read()
                html_data = create_html(data)
                html_data = html_data.replace("b'", "").replace("\\n", "\n")
                return html_data
            return render_template('scanning.html')


    @app.route('/slow_http', methods=['GET', 'POST'])
    def slow_http():
        from utils.slow_http import start_slow_http_attack, check_if_url_is_valid
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