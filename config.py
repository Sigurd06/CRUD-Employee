class Config(object):
    """
    common configurations
    """

class DevelopmentConfig(object):
    """
    Development configuration
    """
    DEBUG = True
    ENV = 'development'
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(object):
    """
    Production configurations
    """
    DEBUG = False
    ENV = 'production'

config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig
}