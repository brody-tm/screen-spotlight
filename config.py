class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:de$1n1by@localhost/movie_review_app'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'abcd'

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
