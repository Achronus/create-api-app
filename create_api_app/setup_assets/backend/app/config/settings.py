import os

from ..utils.fileloader import FileLoader


class Settings:
    __fileloader = FileLoader()

    DIRPATHS = __fileloader.DIRPATHS
    FILEPATHS = __fileloader.FILEPATHS

    DB_URL = os.getenv('DATABASE_URL')
    ENV_TYPE = os.getenv('ENV_TYPE')
    PROJECT_NAME = os.getenv('PROJECT_NAME')
    HOST = os.getenv('HOST')
    PORT = int(os.getenv('PORT'))


settings = Settings()
