import os
import pytest

from conf.constants.filepaths import (
    ProjectPaths, 
    SetupDirPaths, 
    get_project_name,
    set_project_name,
    AssetFilenames,
    SetupAssetsDirNames
)
from conf.constants import STATIC_DIR_NAME

PROJECT_NAME = 'test_project'
SETUP_ROOT = 'create_api_app'

set_project_name(PROJECT_NAME)
CUSTOM_PROJECT_PARENT = get_project_name()
CUSTOM_PROJECT_ROOT = os.path.join(CUSTOM_PROJECT_PARENT)
CUSTOM_PROJECT_BACKEND = os.path.join(CUSTOM_PROJECT_PARENT, 'backend')
CUSTOM_PROJECT_STATIC = os.path.join(CUSTOM_PROJECT_ROOT, 'frontend', STATIC_DIR_NAME)


@pytest.fixture
def project_paths() -> ProjectPaths:
    set_project_name(PROJECT_NAME)
    return ProjectPaths()


def test_project_name_valid(project_paths: ProjectPaths) -> None:
    assert get_project_name() is not None
    assert get_project_name() != ''
    assert get_project_name != project_paths.PROJECT_NAME


class TestProjectPaths:
    @pytest.fixture(autouse=True)
    def initialize_project_paths(self, project_paths) -> None:
        self.project_paths = project_paths

    def __validate_path(self, directory_path: str, ending: str) -> None:
        assert directory_path.endswith(ending), f"Invalid: '{directory_path}' | '{ending}'"

    def test_root_valid(self) -> None:
        self.__validate_path(
            self.project_paths.ROOT, 
            CUSTOM_PROJECT_PARENT
        )

    def test_project_valid(self) -> None:
        self.__validate_path(
            self.project_paths.PROJECT, 
            CUSTOM_PROJECT_ROOT
        )

    def test_init_poetry_conf_valid(self) -> None:
        self.__validate_path(
            self.project_paths.INIT_POETRY_CONF, 
            os.path.join(CUSTOM_PROJECT_ROOT, AssetFilenames.POETRY_CONF)
        )

    def test_init_readme_valid(self) -> None:
        self.__validate_path(
            self.project_paths.INIT_README, 
            os.path.join(CUSTOM_PROJECT_ROOT, AssetFilenames.README)
        )

    def test_poetry_conf_valid(self) -> None:
        self.__validate_path(
            self.project_paths.POETRY_CONF, 
            os.path.join(CUSTOM_PROJECT_BACKEND, AssetFilenames.POETRY_CONF)
        )

    def test_project_build_valid(self) -> None:
        self.__validate_path(
            self.project_paths.BACKEND_BUILD, 
            os.path.join(CUSTOM_PROJECT_BACKEND, AssetFilenames.BUILD)
        )


class TestSetupDirPaths:
    def __validate_path(self, directory_path: str, ending: str) -> None:
        assert directory_path.endswith(ending)

    def test_root_valid(self) -> None:
        self.__validate_path(
            SetupDirPaths.ROOT, 
            os.path.dirname(SETUP_ROOT)
        )

    def test_setup_root_valid(self) -> None:
        self.__validate_path(
            SetupDirPaths.SETUP_ROOT, 
            SETUP_ROOT
        )

    def test_assets_valid(self) -> None:
        self.__validate_path(
            SetupDirPaths.ASSETS, 
            os.path.join(SETUP_ROOT, SetupAssetsDirNames.ROOT)
        )
