"""
api.py
- provides the API endpoints for consuming and producing
  REST requests and responses
"""

from flask import Blueprint, jsonify, request, redirect, url_for

from datetime import *
from dateutil import tz
import dateutil.parser as parser

import bcrypt

from sqlalchemy import func

from flask_login import current_user, login_user, login_required

from .app import login_manager
from .models import db, Sentence, Word, User

import pykakasi

kks = pykakasi.kakasi()
api = Blueprint('api', __name__)

@api.route('/stats', methods=['GET'])
@login_required
def get_stats():
    if request.method == 'GET':
        user_sentences = db.select(Sentence).where(Sentence.user_id == current_user.id).subquery()
        due_words_filter = db.select(Word).where(
            Word.due).where(Word.due <= datetime.now(tz.tzlocal())
        ).join(user_sentences)
        due_words_count = db.session.scalar(db.select(func.count()).select_from(due_words_filter))

        new_sentences_filter = db.select(Sentence).where(Sentence.seen == False)
        new_sentences_count = db.session.scalar(db.select(func.count()).select_from(new_sentences_filter))
        
        return jsonify({'available_words': due_words_count, 
                        'available_sentences': new_sentences_count}), 201
        

@api.route('/sentences', methods=('GET', 'POST'))
@login_required
def fetch_sentences():
    if request.method == 'GET':
        sentences = Sentence.query.filter(Sentence.user_id == current_user.id)
        return jsonify({ 'sentences': [s.to_dict() for s in sentences] })
    elif request.method == 'POST':
        data = request.get_json()

        sentence = Sentence(text=data['sentence'], user_id=current_user.id)
        db.session.add(sentence)
        db.session.flush()

        i=0
        for word in data['words']:          
            word = Word(text=word, gloss=data['gloss'][i], pos=(i+1), sentence_id=sentence.id)
            db.session.add(word)
            i+=1
        
        db.session.commit()
        return jsonify({ 'sentence': sentence.to_dict() }), 201

@api.route('/sentences/<int:id>', methods=['POST'])
@login_required
def update_sentence(id):
    if request.method == 'POST':
        data = request.get_json()
        sentence = db.get_or_404(Sentence, id)
        sentence.due = datetime.now(tz.tzlocal())
        sentence.seen = True
        db.session.add(sentence)

        for word in sentence.words:
            word.due = datetime.now(tz.tzlocal())
            word.seen = True
            db.session.add(word)

        db.session.commit()
        return jsonify( { 'msg': 'success' } ), 201

@api.route('/words/', methods=['GET', 'POST'])
@login_required
def fetch_words():
    if request.method == 'GET':
        user_sentences = db.select(Sentence).where(Sentence.user_id == current_user.id).subquery()
        words_query = db.select(Word).join(user_sentences)
        words = db.session.execute(words_query)
        #words = Word.query.all()
        return jsonify({ 'words': [s.to_dict() for s in words] })

@api.route('/words/<int:id>', methods=['POST'])
@login_required
def update_word(id):
    if request.method == 'POST':
        data = request.get_json()
        
        word = db.get_or_404(Word, id)
        word.due = parser.parse(data.get('due'))
        word.interval = data.get('interval')
        word.last_review=datetime.now(tz.tzlocal())
        word.seen=True
        db.session.add(word)

        sentence = db.get_or_404(Sentence, word.sentence_id)
        sentence.due = parser.parse(data.get('due'))
        sentence.seen=True
        db.session.add(sentence)

        db.session.commit()
        return jsonify({'msg': 'success'}), 201

@api.route('/sentences/<int:id>', methods=('GET', 'PUT'))
@login_required
def get_sentence(id):
    if request.method == 'GET':
        sentence = db.get_or_404(Sentence, id)
        return jsonify(sentence.to_dict())
    elif request.method == 'PUT':
        data = request.get_json()
        #word = db.select(Sentence).where(Sentence.id == data['id'])
    
@api.route('/sentences/new/<int:page>', methods=['GET'])
@login_required
def fetch_new_sentences(page=1, per_page=10):
    if request.method == 'GET':
        result = db.paginate(db.select(Sentence)
                             .where(Sentence.user_id == current_user.id).where(Sentence.seen == False), page=page, per_page=per_page)
        return jsonify({ 'sentences': [sentence.to_dict() for sentence in result], 
                         'next_page': result.next_num, 
                         'prev_page': result.prev_num  }) 
    
@api.route('/sentences/due/<int:page>', methods=['GET'])
@login_required
def fetch_due_sentences(page=1, per_page=50):
    if request.method == 'GET':
        result = db.paginate(db.select(Sentence)
                             .where(Sentence.user_id == current_user.id).where(Sentence.due).where(Sentence.due <= datetime.now(tz.tzlocal()))
                             .order_by(Sentence.due), page=page, per_page=per_page)
        return jsonify({ 'sentences': [sentence.to_dict() for sentence in result], 
                         'next_page': result.next_num, 
                         'prev_page': result.prev_num  }) 
    
@api.route('/words/due/<int:page>', methods=['GET'])
@login_required
def fetch_due_words(page=1, per_page=50):
    if request.method == 'GET':
        user_sentences = db.select(Sentence).where(Sentence.user_id == current_user.id).subquery()
        result = db.paginate(db.select(Word)
                             .where(Word.due).where(Word.due <= datetime.now(tz.tzlocal()))
                             .join(user_sentences)
                             .order_by(Word.due), page=page, per_page=per_page)
        return jsonify({ 'words': [word.to_dict_with_sentence() for word in result], 
                         'next_page': result.next_num, 
                         'prev_page': result.prev_num  }) 
    

@api.route('/sentence/process', methods=['POST'])
@login_required
def process_sentence():
    if request.method == 'POST':
        data = request.get_json()
        parsed_text = [word['orig'] for word in kks.convert(data['sentence'].strip())]
        return jsonify( {'result': parsed_text} ), 201