import bcrypt
import pytest
import os
import sys
import inspect
import jwt

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

import config

from model import UserDao, TweetDao
from service import UserService, TweetService
from sqlalchemy import create_engine, text

database = create_engine(config.test_config['DB_URL'], encoding='utf-8', max_overflow=0)

@pytest.fixture
def user_service():
    return UserService(UserDao(database), config.test_config)

@pytest.fixture
def tweet_service():
    return TweetService(TweetDao(database))

def setup_function():
    ## Create a test user
    hashed_password = bcrypt.hashpw(
        b"testpassword",
        bcrypt.gensalt()
    )
    new_users = [
        {
            'id': 1,
            'name': 'Enwoo Song',
            'email': 'songew@gmail.com',
            'profile': 'test profile',
            'hashed_password': hashed_password
        },
        {
            'id': 2,
            'name': 'Chelsoo Kim',
            'email': 'tet@gmail.com',
            'profile': 'test profile',
            'hashed_password': hashed_password
        }
    ]
    database.execute(text("""
    INSERT INTO users(
        id,
        name,
        email,
        profile,
        hashed_password
    ) VALUES (
        :id,
        :name,
        :email,
        :profile,
        :hashed_password
    )
    """), new_users)

    ## User 2의  Tweet 미리 생성
    database.execute(text("""
    INSERT INTO tweets(
        user_id,
        tweet
    ) VALUES (
        2, 
        "Hello World!"
    )
    """))

def teardown_function():
    database.execute(text("SET FOREIGN_KEY_CHECKS=0"))
    database.execute(text("TRUNCATE users"))
    database.execute(text("TRUNCATE tweets"))
    database.execute(text("TRUNCATE users_follow_list"))
    database.execute(text("SET FOREIGN_KEY_CHECKS=1"))
    # database.execute(text("ALTER TABLE users AUTO_INCREMENT=1"))

def get_user(user_id):
    row = database.execute(text("""
    SELECT
        id,
        name,
        email,
        profile
    FROM users
    WHERE id = :user_id
    """), {
        'user_id': user_id
    }).fetchone()

    return {
        'id': row['id'],
        'name': row['name'],
        'email': row['email'],
        'profile': row['profile']
    } if row else None

def get_follow_list(user_id):
    rows = database.execute(text("""
    SELECT follow_user_id as id
    FROM users_follow_list
    WHERE user_id = :user_id
    """), {
        'user_id': user_id
    }).fetchall()

    return [int(row['id']) for row in rows]

def test_create_new_user(user_service):
    new_user = {
        'name': 'Gildong Hong',
        'email': 'hong@test.com',
        'profile': 'Show up at East and West promptly',
        'password': 'test1234'
    }

    new_user_id = user_service.create_new_user(new_user)
    user = get_user(new_user_id)

    assert user == {
        'id': new_user_id,
        'name': new_user['name'],
        'email': new_user['email'],
        'profile': new_user['profile']
    }

def test_login(user_service):
    # 기 생성되어 있는 사용자의 이메일과 비밀번호를 이용해서 로그인 시도
    assert user_service.login({
        'email': 'songew@gmail.com',
        'password': 'testpassword'
    })

    # 잘못된 비번으로 로그인 시도
    assert not user_service.login({
        'email': 'songew@gmail.com',
        'password': 'test1234'
    })

def test_generate_access_token(user_service):
    # token생성 후 decode하여 동일한 사용자 아이디가 나오는지 테스트
    token = user_service.generate_access_token(1)
    payload = jwt.decode(token, config.JWT_SECRET_KEY, 'HS256')

    assert payload['user_id'] == 1

def test_follow(user_service):
    user_service.follow(1, 2)
    follow_list = get_follow_list(1)

    assert follow_list == [2]

def test_unfollow(user_service):
    user_service.follow(1, 2)
    user_service.unfollow(1, 2)
    follow_list = get_follow_list(1)

    assert follow_list == []

def test_tweet(tweet_service):
    tweet_service.tweet(1, "tweet test")
    timeline = tweet_service.timeline(1)

    assert timeline == [
        {
            'user_id': 1,
            'tweet': 'tweet test'
        }
    ]

def test_timeline(user_service, tweet_service):
    tweet_service.tweet(1, "tweet test")
    tweet_service.tweet(2, "tweet test 2")
    user_service.follow(1, 2)

    timeline = tweet_service.timeline(1)

    assert timeline == [
        {
            'user_id': 2,
            'tweet': 'Hello World!'
        },
        {
            'user_id': 1,
            'tweet': 'tweet test'
        },
        {
            'user_id': 2,
            'tweet': 'tweet test 2'
        }
    ]