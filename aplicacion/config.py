class Config(object):
    SECRET_KEY = 'f0faa2bed03b28e48544762d760aa169'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False

class DevelopmentConfig(Config):
   
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://admin:ZEId3qTQ@172.107.32.120:14196/revision_tecnica"
    SQLALCHEMY_POOL_RECYCLE = 300
    DEBUG = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REDIS_URL = "redis://@redis:6379/0"

    PATH_STORAGE = "/app/tmp"


app_config = {
    'development': DevelopmentConfig,
    
}
