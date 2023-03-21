# https://flask.palletsprojects.com/en/2.2.x/patterns/fileuploads/

class Config(object):
    TESTING = True
    TEMPLATES_AUTO_RELOAD = True
    SECRET_KEY = 'qgERT65=d'
    # Ограничиваем максимально допустимую полезную нагрузку до 16 мегабайт
    MAX_CONTENT_LENGTH = 16 * 1000 * 1000