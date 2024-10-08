class Config:
    SECRET_KEY = "&I^u26560WsJ4?Fl"

class DevelopmentConfig(Config):
    DEBUG = True
    MYSQL_HOST = "localhost"
    MYSQL_USER = "root"
    MYSQL_PASSWORD = ""
    MYSQL_DB = "decoraciones_eventos"

config = {
    'development': DevelopmentConfig
}