import os

from . import STATIC_DIR_NAME


# Setup assets directory names
class SetupAssetsDirNames:
    ROOT = "setup_assets"
    FRONTEND = "frontend"
    BACKEND = "backend"
    APP = "app"


# Asset filenames
class AssetFilenames:
    REQUIREMENTS = "requirements.txt"
    POETRY_CONF = "pyproject.toml"
    README = "README.md"

    MAIN = "main.py"
    BUILD = "build.py"


# Setup assets filepaths
class SetupDirPaths:
    ROOT = os.path.dirname(os.path.join(os.getcwd(), SetupAssetsDirNames.ROOT))
    SETUP_ROOT = os.path.join(ROOT, "create_api_app")
    ASSETS = os.path.join(SETUP_ROOT, SetupAssetsDirNames.ROOT)


def __dotenv_setter(name: str, value: str) -> None:
    os.environ[name] = value


def set_project_name(name: str) -> None:
    __dotenv_setter("PROJECT_NAME", name)


def set_poetry_version(version: str) -> None:
    __dotenv_setter("POETRY_VERSION", version)


def get_project_name() -> str:
    return os.environ.get("PROJECT_NAME")


def get_poetry_version() -> str:
    return os.environ.get("POETRY_VERSION")


# Project directory and filename filepaths
class ProjectPaths:
    def __init__(self, project_name: str = None) -> None:
        self.PROJECT_NAME = project_name if project_name else get_project_name()
        self.ROOT = os.path.join(os.path.dirname(os.getcwd()), self.PROJECT_NAME)
        self.BACKEND = os.path.join(self.ROOT, SetupAssetsDirNames.BACKEND)
        self.BACKEND_APP = os.path.join(self.BACKEND, SetupAssetsDirNames.APP)
        self.FRONTEND = os.path.join(self.ROOT, SetupAssetsDirNames.FRONTEND)

        self.PROJECT = os.path.join(self.ROOT, self.PROJECT_NAME)
        self.INIT_POETRY_CONF = os.path.join(self.PROJECT, AssetFilenames.POETRY_CONF)
        self.INIT_README = os.path.join(self.PROJECT, AssetFilenames.README)

        self.POETRY_CONF = os.path.join(self.BACKEND, AssetFilenames.POETRY_CONF)
        self.BACKEND_BUILD = os.path.join(self.BACKEND, AssetFilenames.BUILD)

        self.STATIC = os.path.join(
            self.ROOT, SetupAssetsDirNames.FRONTEND, STATIC_DIR_NAME
        )

        self.BACKEND_TESTS = os.path.join(self.BACKEND, "tests")
        self.PYTEST_INI = os.path.join(self.BACKEND, "pytest.ini")
        self.PACKAGE_JSON = os.path.join(self.FRONTEND, "package.json")
