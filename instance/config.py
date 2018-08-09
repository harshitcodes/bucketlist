import os

class Config(object):
    """Parent configuration class."""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = "some-very-long-string-of-random-characters-CHANGE-TO-YOUR-LIKING"
    SQLALCHEMY_DATABASE_URI = "postgres://otmymtivsqqnpz:caefb80b1694bed72218ec789ac7fb7f918d91af74d633268865caaa0be38e03@ec2-54-197-253-122.compute-1.amazonaws.com:5432/d4qc50r0cimhs8"

class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True

class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/test_db'
    DEBUG = True

class StagingConfig(Config):
    """Configurations for Staging."""
    DEBUG = True

class ProductionConfig(Config):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False

app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}
