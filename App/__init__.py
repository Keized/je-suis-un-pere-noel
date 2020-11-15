import os
from flask import Flask

from .routes import app
from . import models

# Connect sqlalchemy to app
models.db.init_app(app)


@app.cli.command('init-db')
def init_db():
    models.init_db()
