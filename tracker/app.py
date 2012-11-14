from flask import Flask
from views.announce import announce


app = Flask(__name__)
app.register_blueprint(announce)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
