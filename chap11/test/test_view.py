# pytest -vv -s -p no:warning

import bcrypt
import pytest
import json
import os
import io
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

import config

from app import create_app
from sqlalchemy import create_engine, text
from unittest import mock

database = create_engine(config.test_config['DB_URL'], encoding='utf-8', max_overflow=0)

@pytest.fixture
@mock.patch("app.boto3")
def api(mock_boto3):
    mock_boto3.client.return_value = mock.Mock()

    app = create_app(config.test_config)
    app.config['TEST'] = True
    api = app.test_client()

    return api

def test_ping(api):
    resp = api.get('/ping')
    assert b'pong' in resp.data

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

def test_login(api):
    resp = api.post(
        '/login',
        data = json.dumps({'email': 'songew@gmail.com', 'password': 'testpassword'}),
        content_type = 'application/json'
    )
    assert b"access_token" in resp.data

def test_unauthorized(api):
    # access token없는 경우 401 응답 Return확인
    resp = api.post(
        '/tweet',
        data = json.dumps({'tweet': "Hello World!"}),
        content_type = 'application/json'
    )
    assert resp.status_code == 401

    resp = api.post(
        '/follow',
        data = json.dumps({'follow': 2}),
        content_type = 'application/json'
    )
    assert resp.status_code == 401

    resp = api.post(
        '/unfollow',
        data = json.dumps({'unfollow': 2}),
        content_type = 'application/json'
    )
    assert resp.status_code == 401

def test_tweet(api):
    ## login
    resp = api.post(
        '/login',
        data = json.dumps({
            'email': 'songew@gmail.com',
            'password': 'testpassword'
            }),
        content_type = 'application/json'
    )
    resp_json = json.loads(resp.data.decode('utf-8'))
    access_token = resp_json['access_token']

    ## tweet
    resp = api.post(
        '/tweet',
        data = json.dumps({
            'tweet': 'Hello World!'
        }),
        content_type='application/json',
        headers = {'Authorization': access_token}
    )
    assert resp.status_code == 200

    ## check tweet
    resp = api.get(f'/timeline/1')
    tweets = json.loads(resp.data.decode('utf-8'))

    assert resp.status_code == 200
    assert tweets == {
        'user_id': 1,
        'timeline': [
            {
                'user_id': 1,
                'tweet': 'Hello World!'
            }
        ]
    }

def test_follow(api):
    # login
    resp = api.post(
        '/login',
        data = json.dumps({
            'email': 'songew@gmail.com', 
            'password': 'testpassword'}),
        content_type = 'application/json'
    )
    resp_json = json.loads(resp.data.decode('utf-8'))
    access_token = resp_json['access_token']

    ## 먼저 사용자 1의 tweet을 확인하여 tweet리스트가 비어 있는 것을 확인
    resp = api.get(f'/timeline/1')
    tweets = json.loads(resp.data.decode('utf-8'))
    assert resp.status_code == 200
    assert tweets == {
        'user_id': 1,
        'timeline': []
    }

    ## follow UserId = 2
    resp = api.post(
        '/follow',
        data = json.dumps({'follow': 2}),
        content_type = 'application/json',
        headers = {'Authorization': access_token}
    )
    assert resp.status_code == 200

    ## 이제 사용자 1의 tweet을 확인해서 사용자 2의 tweet이 리턴되는 것을 확인
    resp = api.get(f'/timeline/1')
    tweets = json.loads(resp.data.decode('utf-8'))

    assert resp.status_code == 200
    assert tweets == {
        'user_id': 1,
        'timeline': [
            {
                'user_id': 2,
                'tweet': 'Hello World!'
            }
        ]
    }

def test_unfollow(api):
    # login
    resp = api.post(
        '/login',
        data = json.dumps({
            'email': 'songew@gmail.com', 
            'password': 'testpassword'}),
        content_type = 'application/json'
    )
    resp_json = json.loads(resp.data.decode('utf-8'))
    access_token = resp_json['access_token']

    ## follow UserId = 2
    resp = api.post(
        '/follow',
        data = json.dumps({'follow': 2}),
        content_type = 'application/json',
        headers = {'Authorization': access_token}
    )
    assert resp.status_code == 200

    ## 이제 사용자 1의 tweet을 확인해서 사용자 2의 tweet이 리턴되는 것을 확인
    resp = api.get(f'/timeline/1')
    tweets = json.loads(resp.data.decode('utf-8'))

    assert resp.status_code == 200
    assert tweets == {
        'user_id': 1,
        'timeline': [
            {
                'user_id': 2,
                'tweet': 'Hello World!'
            }
        ]
    }

    ## unfollow UserId = 2
    resp = api.post(
        '/unfollow',
        data = json.dumps({'unfollow': 2}),
        content_type = 'application/json',
        headers = {'Authorization': access_token}
    )
    assert resp.status_code == 200

    ## 이제 사용자 1의 tweet을 확인해서 사용자 2의 tweet이 더이상 리턴되지 않는 것을 확인
    resp = api.get(f'/timeline/1')
    tweets = json.loads(resp.data.decode('utf-8'))

    assert resp.status_code == 200
    assert tweets == {
        'user_id': 1,
        'timeline': []
    }

def test_save_and_get_profile_picture(api):
    # login
    resp = api.post(
        '/login',
        data = json.dumps({
            'email': 'songew@gmail.com', 
            'password': 'testpassword'}),
        content_type = 'application/json'
    )
    resp_json = json.loads(resp.data.decode('utf-8'))
    access_token = resp_json['access_token']

    # upload image file
    resp = api.post(
        '/profile-picture',
        content_type = 'multipart/form-data',
        headers = {'Authorization': access_token},
        data = {'profile_pic': (io.BytesIO(b'some image here'), 'profile.png')}
    )
    assert resp.status_code == 200

    # get image url
    resp = api.get('/profile-picture/1')
    data = json.loads(resp.data.decode('utf-8'))

    assert data['img_url'] == f"{config.test_config['S3_BUCKET_URL']}profile.png"