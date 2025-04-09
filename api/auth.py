"""
auth.py
- provides the API endpoints for consuming and producing
  REST requests and responses
"""
from datetime import datetime, timedelta
import jwt
import bcrypt
from flask import Blueprint, jsonify, request, current_app
from flask_login import current_user, login_user, logout_user, login_required

from api.models import db, User, UserToken

auth = Blueprint('auth', __name__)

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

@auth.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        email = request.get_json()['email']
        username = request.get_json()['username']
        password = request.get_json()['password']
        user = User(email, username, password)
        db.session.add(user)
        db.session.commit()
        return jsonify({ 'message': 'success' }), 200

@auth.route('/protected')
@login_required
def protected():
    return 'Logged in as: ' + current_user.username