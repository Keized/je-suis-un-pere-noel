from flask import Blueprint, jsonify, abort
from app.models import User
from app.auth.controllers import auth_required

users_mod = Blueprint('users', __name__, url_prefix='/')


@users_mod.route('/api/users', methods=['GET'])
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


@users_mod.route('/api/users/<int:id>')
def get_user(id):
    user = User.query.get(id)
    if not user:
        abort(400)
    return jsonify({'username': user.username})
