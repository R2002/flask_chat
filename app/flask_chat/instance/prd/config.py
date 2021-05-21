import os
#--------------------------------------#
# 設定ファイル
#--------------------------------------#
# 環境
ENV = 'production'
DEBUG = False

# DB設定
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}/{db_name}?charset=utf8'.format(**{
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'host': os.getenv('DB_HOST', 'localhost'),
    'db_name': 'flask_chat',
})
SECRET_KEY = 'secret!'

# ルーティング設定
APPLICATION_ROOT = 'flask_chat/'