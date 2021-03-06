from flask import Flask

app = Flask('app')

if __name__ == '__main__':
    from core.core import create_app
    create_app().run(debug=False, host='0.0.0.0', port=80, threaded=True)