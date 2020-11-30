from flask import Flask, request, jsonify, abort, url_for, g, make_response
from flask_httpauth import HTTPBasicAuth
from .models import User, db
from functools import wraps
from datetime import datetime, timedelta

import jwt

app = Flask(__name__)
auth = HTTPBasicAuth()

# Config options - Make sure you created a 'config.py' file.
app.config.from_object('config')


def auth_required(func):
    def wrap(*args, **kwargs):
        token = None
        current_user = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            abort(401, 'Token missing')

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query \
                .filter_by(email=data['email']) \
                .first()
        except:
            abort(401, 'Token Invalid')

        return func(current_user, *args, **kwargs)


    return wrap


@app.route('/api/users', methods=['GET'])
@auth_required
def get_all_users(current_user):
    users = User.query.all()
    output = []
    for user in users:
        output.append({
            'id': user.id,
            'username': user.username,
            'email': user.email
        })

    return jsonify({'users': output})


@app.route('/api/users/<int:id>')
def get_user(id):
    user = User.query.get(id)
    if not user:
        abort(400)
    return jsonify({'username': user.username})


@app.route('/api/login', methods=['POST'])
def login():
    email = request.json.get('email')
    username = request.json.get('username')
    password = request.json.get('password')

    if password is None or email is None:
        abort(401, 'Invalid email or Password')

    user = User.query \
        .filter_by(email=email) \
        .first()

    if not user:
        abort(401, 'User not found')

    if user.verify_password(password):
        token = jwt.encode({
            'email': user.email,
            'exp': datetime.utcnow() + timedelta(minutes=30)
        }, app.config['SECRET_KEY'])

        return make_response(jsonify({'token': token.decode('UTF-8')}), 201)
    abort(401, 'Wrong password')


@app.route('/api/register', methods=['POST'])
def register():
    email = request.json.get('email')
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None or email is None:
        abort(400, 'Invalid Payload')
    if User.query.filter_by(email=email).first() is not None:
        abort(400, 'User already exists')
    user = User(email=email, username=username, password=password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'username': user.username}), 201, {'Location': url_for('get_user', id=user.id, _external=True)}
