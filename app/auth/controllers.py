from flask import Blueprint, jsonify, request, abort, make_response, url_for
from datetime import datetime, timedelta
from app.models import User
import jwt
import app

auth_mod = Blueprint('auth', __name__, url_prefix='/')


def auth_required(func):
    def wrap(*args, **kwargs):
        token = None
        current_user = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            abort(401, 'Token missing')

        try:
            data = jwt.decode(token, app.app.config['SECRET_KEY'])
            current_user = User.query \
                .filter_by(email=data['email']) \
                .first()
        except:
            abort(401, 'Token Invalid')
        return func(current_user, *args, **kwargs)

    return wrap


@auth_mod.route('/api/login', methods=['POST'])
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
        }, app.app.config['SECRET_KEY'])

        return make_response(jsonify({'token': token.decode('UTF-8')}), 201)
    abort(401, 'Wrong password')


@auth_mod.route('/api/register', methods=['POST'])
def register():
    email = request.json.get('email')
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None or email is None:
        abort(400, 'Invalid Payload')
    if User.query.filter_by(email=email).first() is not None:
        abort(400, 'User already exists')
    user = User(email=email, username=username, password=password)
    app.db.session.add(user)
    app.db.session.commit()
    return jsonify({'username': user.username}), 201, {'Location': url_for('get_user', id=user.id, _external=True)}
