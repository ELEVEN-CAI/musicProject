class Config():
    DEBUG = True
    ENV = 'development'
    SECRET_KEY = 'akdikska8&&8&&$#%'

    # mysql数据库连接
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@127.0.0.1:3306/users'
    SQLALCHEMY_TRACK_MODIFICATIONS = False