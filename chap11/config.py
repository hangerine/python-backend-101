db = {
    'user': 'root',
    'password': 'qwer1234',
    'host': 'database-1.ctlsetaj2jig.ap-northeast-2.rds.amazonaws.com',
    'port': 3306,
    'database': 'miniter'
}

JWT_SECRET_KEY = 'secret'
JWT_EXP_DELTA_SECONDS = 7 * 24 * 60 * 60
UPLOAD_DIRECTORY = './profile_pictures'
DB_URL = f"mysql+mysqlconnector://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?charset=utf8"

S3_BUCKET = "python-backend-s3"
S3_ACCESS_KEY = "AKIARCGL4HLSVSPTZI5F"
S3_SECRET_KEY = "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"
S3_BUCKET_URL = f"http://{S3_BUCKET}.s3.amazonaws.com/"

test_db = {
    'user': 'root',
    'password': 'secret',
    'host': 'localhost',
    'port': 3306,
    'database': 'miniter'
}

test_config = { 
    'DB_URL': f"mysql+mysqlconnector://{test_db['user']}:{test_db['password']}@{test_db['host']}:{test_db['port']}/{test_db['database']}?charset=utf8",
    'JWT_SECRET_KEY': 'secret',
    'JWT_EXP_DELTA_SECONDS': 7 * 24 * 60 * 60,
    "S3_BUCKET": "python-backend-s3",
    "S3_ACCESS_KEY": "test_access_key",
    "S3_SECRET_KEY": "test_secret_key",
    "S3_BUCKET_URL": f"http://test_s3.amazonaws.com/"
}