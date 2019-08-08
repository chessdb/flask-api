import sentry_sdk
from flask import Flask
from sentry_sdk.integrations.flask import FlaskIntegration

import config
from src.api.v1 import API
from src.extensions import MIGRATE, DB, CELERY


def create_app(app_config=config.ProductionConfig):
    app = Flask(__name__)
    app.config.from_object(app_config)
    initialize_extensions(app=app)
    register_blueprints(app=app)
    return app


def register_blueprints(app: Flask):
    from src.api.v1 import API_V1
    app.register_blueprint(API_V1)


def initialize_extensions(app: Flask):
    DB.init_app(app=app)

    MIGRATE.init_app(app=app, db=DB)

    sentry_sdk.init(
        integrations=[FlaskIntegration()],
        release="0.0.1",
        send_default_pii=True
    )

    CELERY.config_from_object(app.config)
