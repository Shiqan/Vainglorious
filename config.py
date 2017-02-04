class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_POOL_RECYCLE = 299
    SQLALCHEMY_TRACK_MODIFACTION = False

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
        username="shiqan",
        password="plainpasswordftw",
        hostname="shiqan.mysql.pythonanywhere-services.com",
        databasename="shiqan$vainglory",
    )

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql://{username}:{password}@{hostname}/{databasename}".format(
        username="root",
        password="root",
        hostname="localhost:3306",
        databasename="vainglory"
    )