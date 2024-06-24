import os

from app.utils.fileloader import FileLoader


class Settings:
    __fileloader = FileLoader()

    DIRPATHS = __fileloader.DIRPATHS
    FILEPATHS = __fileloader.FILEPATHS

    DB_URL = os.getenv("DATABASE_URL")
    DB_NAME = ""  # Update me!
    DB_COLLECTION_NAME = ""  # Update me!


settings = Settings()
