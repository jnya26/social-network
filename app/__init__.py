from flask import Flask
from config import Config
from flask_login import current_user
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()


def create_app():
    """
    Application factory method to create application
    :return: Flask application configured object
    """

    # create instance of Flask object
    app = Flask(__name__)

    # update application config from Config class in config.py
    app.config.from_object(Config)

    # install extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # register blueprints here
    from .main import bp as main_bp
    app.register_blueprint(main_bp)

    from .auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from .faker import bp as fake_bp
    app.register_blueprint(fake_bp)

    from . import models  # noqa

    @app.context_processor
    def context_processor():
        return dict(
            current_user=current_user
        )

    return app


# create instance of application
app = create_app()
