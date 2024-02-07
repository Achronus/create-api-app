import os
import textwrap

from .filepaths import ProjectPaths


# FastAPI directory and filenames names
class FastAPIDirnames:
    DATABASE = 'db'


class FastAPIFilenames:
    BASE = '__init__.py'


# FastAPI directory filepaths
class FastAPIDirPaths:
    def __init__(self) -> None:
        project_paths = ProjectPaths()

        self.DATABASE_DIR = os.path.join(project_paths.BACKEND_APP, FastAPIDirnames.DATABASE)
        self.DATABASE_INIT_FILE = os.path.join(self.DATABASE_DIR, FastAPIFilenames.BASE)


# Define extra content
class FastAPIContent:
    SQLITE_DB_POSITION = "os.getenv('DATABASE_URL')"
    SQLITE_DB_CONTENT = ', connect_args={"check_same_thread": False}'

    PYTEST_INI = textwrap.dedent("""
    [pytest]
    env_files =
        backend/.env.local
        .env.prod

    addopts = -v -s
    """)[1:]
