from config import Config
from flask import Flask


def creat_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from .auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from .main import bp as main_bp
    app.register_blueprint(main_bp)

    return app

app = creat_app()
from .main import routes


