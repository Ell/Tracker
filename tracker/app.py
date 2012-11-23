from flask import Flask
from announce import announce


def create_app(config):
	app = Flask(__name__)
	app.config.from_pyfile(config)

	#blueprints
	app.register_blueprint(announce)

	return app
