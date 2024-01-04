from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_migrate import Migrate
import flask_login

login_manager = flask_login.LoginManager()

def create_app(app_name='SURVEY_API'):
    app = Flask(app_name)
    app.config.from_object('api.config.BaseConfig')

    # enable CORS
    CORS(app, resources={r'/*': {'origins': '*'}})

    from api.api import api
    app.register_blueprint(api, url_prefix="/api")

    from api.auth import auth
    app.register_blueprint(auth, url_prefix="/auth")

    from api.models import db
    migrate = Migrate(app, db)
 
    login_manager.init_app(app)
    
    db.init_app(app)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run()