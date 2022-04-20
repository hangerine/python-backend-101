db = {
    'user': 'root',
    'password': 'qwer1234',
    'host': 'database-1.ctlsetaj2jig.ap-northeast-2.rds.amazonaws.com',
    'port': 3306,
    'database': 'miniter'
}

JWT_SECRET_KEY = 'secret'
DB_URL = f"mysql+mysqlconnector://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?charset=utf8"

test_config = { 
    'DB_URL': f"mysql+mysqlconnector://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?charset=utf8",
    'JWT_SECRET_KEY': 'secret'
}