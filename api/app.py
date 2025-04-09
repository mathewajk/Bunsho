from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import flask_login

login_manager = flask_login.LoginManager()

def create_app(app_name='BUNSHO'):
    app = Flask(app_name)
    app.config.from_object('settings')

    # enable CORS
    CORS(app, resources={r'/*': {'origins': app.config['ALLOWED_HOSTS']}})

    from bunsho import api
    app.register_blueprint(api, url_prefix="/api")

    from auth import auth
    app.register_blueprint(auth, url_prefix="/auth")

    from models import db, login_manager
    migrate = Migrate(app, db)
    login_manager.init_app(app)
    
    db.init_app(app)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run()
else:
    gunicorn_app = create_app()