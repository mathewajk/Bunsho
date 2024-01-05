"""
models.py
- Data classes for the surveyapi application
"""

from datetime import datetime, timedelta
import jwt, bcrypt

from flask import current_app, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

from bcrypt import hashpw, gensalt

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    authenticated = db.Column(db.Boolean, default=False)

    sentences = db.relationship('Sentence', backref="user", lazy=False)

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = hashpw(bytes(password, 'utf-8'), gensalt())

    def get_id(self):
        return self.email
    
    def to_dict(self):
        return dict(id=self.id, username=self.username, email=self.email)
    
    def authenticate(self, password):
        return bcrypt.checkpw(bytes(password, 'utf-8'), bytes(self.password, 'utf-8'))
    
    def generate_token(self):
        token = UserToken(user_id=self.id, sub=self.email, iat=datetime.utcnow(), exp=datetime.utcnow() + timedelta(days=1))
        db.session.add(token)
        db.session.commit()
        return token
    
    def refresh_token(self):
        query = db.select(UserToken).where(UserToken.user_id == self.id).order_by(UserToken.exp.desc())
        token = db.session.execute(query).first()[0]
        if(self.is_authenticated):
            token.iat=datetime.utcnow()
        else:
            token.iat=datetime.utcnow()
            token.exp=datetime.utcnow()
        db.session.add(token)
        db.session.commit()
        return token

class UserToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    sub = db.Column(db.String(100), nullable=False)
    iat = db.Column(db.DateTime, nullable=False)
    exp = db.Column(db.DateTime, nullable=False)

    def encode_token(self):
        return jwt.encode({
            'sub': self.sub,
            'iat': self.iat,
            'exp': self.exp}, current_app.config['SECRET_KEY'], algorithm="HS256")

class Sentence(db.Model):
    __tablename__ = 'sentences'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    text = db.Column(db.Text, nullable=False)
    #punctuation = db.Column(db.Text, nullable=True)
    words = db.relationship('Word', backref="sentence", lazy=False)

    seen = db.Column(db.Boolean, default=False, nullable=False)
    due = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        return dict(id=self.id,
                    created_at=self.created_at.isoformat(),
                    text=self.text,
                    words=[word.to_dict() for word in sorted(self.words, key=(lambda word: word.pos))],
                    seen=self.seen,
                    due=self.due.isoformat() if self.due else None)

class Word(db.Model):
    __tablename__ = 'words'

    id          = db.Column(db.Integer, primary_key=True)
    sentence_id = db.Column(db.Integer, db.ForeignKey('sentences.id'))
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)

    text  = db.Column(db.String(500), nullable=False)
    gloss = db.Column(db.String(500), nullable=False)
    pos   = db.Column(db.Integer, nullable=False)
   
    seen        = db.Column(db.Boolean, nullable=False, default=False)
    last_review = db.Column(db.DateTime, nullable=True)
    due         = db.Column(db.DateTime, nullable=True)
    
    interval      = db.Column(db.Integer, nullable=False, default=1)
    easing_factor = db.Column(db.Integer, nullable=False, default=2.5)

    def to_dict(self):
        return dict(id=self.id,
                    text=self.text,
                    gloss=self.gloss,
                    pos=self.pos)
    
    def to_dict_with_sentence(self):
        base_json = self.to_dict()
        base_json.update(dict(sentence_id=self.sentence_id),
                         created_at=self.created_at.isoformat(),
                         seen=self.seen,
                         last_review=self.last_review.isoformat() if self.last_review else None,
                         due=self.due.isoformat() if self.due else None,
                         interval=self.interval,
                         easing_factor=self.easing_factor)
                         
        return dict(word=base_json,
                    sentence=self.sentence.to_dict())
