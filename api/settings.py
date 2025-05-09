from environs import env

env.read_env()

DEBUG = env.bool('FLASK_DEBUG', default=False)
ALLOWED_HOSTS = env.list('FLASK_ALLOWED_HOSTS', default=['http://localhost:5173'])
SECRET_KEY = env.str('FLASK_SECRET_KEY', default='default')

SQLALCHEMY_DATABASE_URI = env.str('SQLALCHEMY_DATABASE_URI')
SQLALCHEMY_TRACK_MODIFICATIONS = False

# SESSION_COOKIE_HTTPONLY=True
# REMEMBER_COOKIE_HTTPONLY=True
# SESSION_COOKIE_SAMESITE="Lax"
# SESSION_COOKIE_SECURE = True
# REMEMBER_COOKIE_SECURE = True