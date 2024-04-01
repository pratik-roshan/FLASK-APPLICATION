from functools import wraps
from flask import g, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User

def auth_required_with_permission(permission):
    def decorator(func):
        @wraps(func)
        @jwt_required()
        def wrapper(*args, **kwargs):
            current_user = get_jwt_identity()
            user = User.get_user_by_username(current_user)
            if not user:
                abort(401, 'Unauthorized')

            if permission not in [p.permission_name for r in user.roles for p in r.permissions]:
                abort(403, 'Forbidden')
            return func(*args, **kwargs)
        return wrapper
    return decorator
