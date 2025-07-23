from functools import wraps
from flask import redirect, url_for, session

def login_required(f):
    @wraps(f)
    def decorated_function( ):
        if "username" not in session:
            return redirect(url_for('login_get'))
        return f( )
    return decorated_function