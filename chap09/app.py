import config

from flask import Flask
from sqlalchemy import create_engine
from flask_cors import CORS

from model import UserDao, TweetDao
from service import UserService, TweetService
from view import create_endpoint

class Services:
    pass

def create_app(test_config=None):
    app = Flask(__name__)

    CORS(app)

    if test_config is None:
        app.config.from_pyfile("config.py")
    else:
        app.config.update(test_config)

    database = create_engine(app.config['DB_URL'], encoding='UTF-8', max_overflow=0)

    # Persistence
    user_dao = UserDao(database)
    tweet_dao = TweetDao(database)

    # Business Layer
    services = Services
    services.user_service = UserService(user_dao, app.config)
    services.tweet_service = TweetService(tweet_dao)

    # Create endpoints
    create_endpoint(app, services)

    return app