# import os
# from flask import Flask
#
# from .routes import app
# from . import models
#
# # Connect sqlalchemy to app
# models.db.init_app(app)
#
#
# @app.cli.command('init-db')
# def init_db():
#     models.init_db()
#
#

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.auth.controllers import auth_mod
from app.users.controllers import users_mod
from app.events.controllers import events_mod

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

app.register_blueprint(auth_mod)
app.register_blueprint(users_mod)


# db.create_all()

# def init_db():
#     db.drop_all()
#     db.create_all()app
#     db.session.add(Event("Noël 2021"))
#     db.session.commit()
#     lg.warning('Database initialized!')
