"""
auth.py
- provides the API endpoints for consuming and producing
  REST requests and responses
"""
from datetime import datetime, timedelta
import jwt

from flask import Blueprint, jsonify, request, current_app
from flask_login import current_user, login_user, logout_user, login_required

from .app import login_manager
from .models import db, User, UserToken

import bcrypt

auth = Blueprint('auth', __name__)

@login_manager.user_loader
def user_loader(user_id):
    query = db.select(User).where(User.email == user_id)
    return db.session.execute(query).last()[0]

@login_manager.request_loader
def request_loader(request):
    auth = request.headers.get('Authorization')
    try: 
        token = jwt.decode(auth, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        query = db.select(User).where(User.email == token.get('sub'))
        return db.session.execute(query).first()[0]
    except:
        return None

@auth.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.get_json()['username']
        password = request.get_json()['password']
        user_query = db.select(User).where(User.username == username)
        user = db.session.execute(user_query).first()[0]
        if user and user.authenticate(password):
            login_user(user, remember=True)
            token = user.generate_token()
            return jsonify({
                'message': 'success',
                'token': token.encode_token(),
                'user': user.to_dict()
            })
        return jsonify({ 'message': 'Invalid credentials', 'authenticated': False }), 401
    
@auth.route('/logout', methods=['POST'])
def logout():
    if request.method == 'POST':
        username = request.get_json()['username']
        user_query = db.select(User).where(User.username == username)
        user = db.session.execute(user_query).first()[0]
        if user:
            logout_user()
            return jsonify({
                'message': 'success',
            })
        return jsonify({ 'message': 'User not found' }), 404

@auth.route('/token', methods=['GET'])
def token():
    if request.method == 'GET':
        try: 
            token = current_user.refresh_token()
            return jsonify({ 'token': token.encode_token(),
                             'user': current_user.to_dict() })
        except:
            return jsonify({ 'token': None,
                             'user': None })

    
@auth.route('/protected')
@login_required
def protected():
    return 'Logged in as: ' + current_user.username