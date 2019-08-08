from celery import Celery
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()
MIGRATE = Migrate()
CELERY = Celery()
