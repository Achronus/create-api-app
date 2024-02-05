import os

from . import STATIC_DIR_NAME
from ..helper import set_tw_standalone_filename


# Setup assets directory names
class SetupAssetsDirNames:
    ROOT = 'setup_assets'
    FRONTEND = 'frontend'
    BACKEND = 'backend'

    CSS = 'css'
    JS = 'js'
    IMGS = 'imgs'

    CONFIG = 'config'
    DOCKERFILES = 'docker'


# Asset filenames
class AssetFilenames:
    _js_ext = '.min.js'
    _css_ext = '.min.css'

    TW_STANDALONE = set_tw_standalone_filename()
    ALPINE = 'alpine' + _js_ext
    HTMX = 'htmx' + _js_ext
    FLOWBITE_CSS = 'flowbite' + _css_ext
    FLOWBITE_JS = 'flowbite' + _js_ext

    REQUIREMENTS = 'requirements.txt'
    POETRY_CONF = 'pyproject.toml'
    README = 'README.md'
    
    LOCAL_ENV = '.env.local'
    PROD_ENV = '.env.prod'

    MAIN = 'main.py'
    BUILD = 'build.py'


# Asset URLs
class AssetUrls:
    TW_STANDALONE = 'https://github.com/tailwindlabs/tailwindcss/releases/latest/download/'
    ALPINE = 'node_modules/alpinejs/dist/cdn.min.js'
    HTMX = f'https://unpkg.com/htmx.org/dist/{AssetFilenames.HTMX}'
    FLOWBITE_CSS = f'node_modules/flowbite/dist/{AssetFilenames.FLOWBITE_CSS}'
    FLOWBITE_JS = f'node_modules/flowbite/dist/{AssetFilenames.FLOWBITE_JS}'


# Static folder directory names
class StaticDirNames:
    ROOT = os.path.join(os.getcwd(), STATIC_DIR_NAME, SetupAssetsDirNames.FRONTEND)
    CSS = os.path.join(ROOT, SetupAssetsDirNames.CSS)
    JS = os.path.join(ROOT, SetupAssetsDirNames.JS)
    IMGS = os.path.join(ROOT, SetupAssetsDirNames.IMGS)


# Setup assets filepaths
class SetupDirPaths:
    ROOT = os.path.dirname(os.path.join(os.getcwd(), SetupAssetsDirNames.ROOT))
    SETUP_ROOT = os.path.join(ROOT, 'create_api_app')
    ASSETS = os.path.join(SETUP_ROOT, SetupAssetsDirNames.ROOT)
    PROJECT_NAME = os.path.join(SETUP_ROOT, 'conf', 'name')


def __dotenv_setter(name: str, value: str) -> None:
    os.environ[name] = value


def set_project_name(name: str) -> None:
    __dotenv_setter('PROJECT_NAME', name)


def set_db_url(url: str) -> None:
    __dotenv_setter('DATABASE_URL', url)


def set_poetry_version(version: str) -> None:
    __dotenv_setter('POETRY_VERSION', version)


def get_project_name() -> str:
    return os.environ.get('PROJECT_NAME')


def get_db_url() -> str:
    return os.environ.get('DATABASE_URL')


def get_poetry_version() -> str:
    return os.environ.get('POETRY_VERSION')


# Project directory and filename filepaths
class ProjectPaths:
    def __init__(self) -> None:
        self.PROJECT_NAME = get_project_name()
        self.ROOT = os.path.join(os.path.dirname(os.getcwd()), self.PROJECT_NAME)
        self.BACKEND = os.path.join(self.ROOT, SetupAssetsDirNames.BACKEND)
        self.FRONTEND = os.path.join(self.ROOT, SetupAssetsDirNames.FRONTEND)

        self.PROJECT = os.path.join(self.ROOT, self.PROJECT_NAME)
        self.INIT_POETRY_CONF = os.path.join(self.PROJECT, AssetFilenames.POETRY_CONF)
        self.INIT_README = os.path.join(self.PROJECT, AssetFilenames.README)
        
        self.POETRY_CONF = os.path.join(self.ROOT, AssetFilenames.POETRY_CONF)
        self.PROJECT_MAIN = os.path.join(self.ROOT, AssetFilenames.MAIN)
        self.PROJECT_BUILD = os.path.join(self.ROOT, AssetFilenames.BUILD)

        self.STATIC = os.path.join(self.ROOT, SetupAssetsDirNames.FRONTEND, STATIC_DIR_NAME)
        self.CSS = os.path.join(self.STATIC, SetupAssetsDirNames.CSS)
        self.JS = os.path.join(self.STATIC, SetupAssetsDirNames.JS)
        self.IMGS = os.path.join(self.STATIC, SetupAssetsDirNames.IMGS)


# Dockerfile specific directory and filename filepaths
class DockerPaths:
    def __init__(self) -> None:
        self.df = 'Dockerfile'
        self.compose = 'docker-compose'

        self._yml_ext = '.yml'
        self._project_root = os.path.dirname(os.getcwd())

        self.ROOT_DIR = os.path.join(self._project_root, SetupAssetsDirNames.CONFIG, SetupAssetsDirNames.DOCKERFILES)

        self.BACKEND_DF = os.path.join(self.ROOT_DIR, f'{self.df}.backend')
        self.IGNORE = os.path.join(self._project_root, '.dockerignore')
        
        self.COMPOSE_BASE = os.path.join(self._project_root, f"{self.compose}.base{self._yml_ext}")
        self.COMPOSE_MAIN = os.path.join(self._project_root, f"{self.compose}{self._yml_ext}")
