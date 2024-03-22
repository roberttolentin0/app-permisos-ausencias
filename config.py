# from decouple import config

# SQLITE = "sqlite:///project.db"
# POSTGRESQL = "postgresql+psycopg2://postgres:123456@localhost:5432/blogposts_db"

class Config():
    DEBUG = True
    SECRET_KEY = 'dev'


class DevelopmentConfig(Config):
    DEBUG = True

class ProductConfig(Config):
    DEBUG = False

config = {
    'development': ProductConfig
}