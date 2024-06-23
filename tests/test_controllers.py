import os
import pytest

from create_api_app.conf.constants import BACKEND_CORE_PACKAGES, BACKEND_DEV_PACKAGES
from create_api_app.conf.constants.filepaths import ProjectPaths
from create_api_app.setup.backend import VEnvController
from tests.mappings.pytoml import TOML_DESCRIPTION


@pytest.fixture
def project_name() -> str:
    return "_pytest_demo"


@pytest.fixture
def project_dir(project_name: str) -> str:
    return os.path.join(os.getcwd(), project_name)


@pytest.fixture
def backend_dir(project_dir: str) -> str:
    return os.path.join(project_dir, "backend")


@pytest.fixture
def frontend_dir(project_dir: str) -> str:
    return os.path.join(project_dir, "frontend")


@pytest.fixture
def asset_dir() -> str:
    return os.path.join(os.getcwd(), "create_api_app", "setup_assets")


def get_filepaths(dir_filepath: str) -> list[str]:
    files = []
    for file in os.listdir(dir_filepath):
        sub_file = os.path.join(dir_filepath, file)
        if os.path.isdir(sub_file):
            sub_files = os.listdir(sub_file)

            for f in sub_files:
                files.append(os.path.join(sub_file, f))

        files.append(sub_file)

    return files


class TestInitConfig:
    @staticmethod
    def test_backend_dir_exists(backend_dir: str):
        assert os.path.exists(backend_dir)

    @staticmethod
    def test_frontend_dir_exists(frontend_dir: str):
        assert os.path.exists(frontend_dir)


class TestVEnvController:
    @pytest.fixture
    def controller(self, project_name: str) -> VEnvController:
        return VEnvController(
            project_paths=ProjectPaths(project_name),
        )

    @staticmethod
    def test_project_name(controller: VEnvController, project_name: str):
        assert controller.project_paths.PROJECT_NAME == project_name

    @staticmethod
    def test_project_root(controller: VEnvController, project_name: str):
        assert controller.project_paths.ROOT == os.path.join(
            os.path.dirname(os.getcwd()), project_name
        )

    @staticmethod
    def test_toml_description(backend_dir: str):
        filepath = os.path.join(backend_dir, "pyproject.toml")

        with open(filepath, "r") as f:
            lines = f.readlines()

        assert lines[:10] == TOML_DESCRIPTION

    @staticmethod
    def test_toml_core_dependencies(backend_dir: str):
        filepath = os.path.join(backend_dir, "pyproject.toml")

        with open(filepath, "r") as f:
            lines = f.readlines()

        count = 0
        for item in BACKEND_CORE_PACKAGES:
            for line in lines[10:]:
                if line.startswith(item.split("[")[0]):
                    count += 1
                    break

        assert count == len(BACKEND_CORE_PACKAGES)

    @staticmethod
    def test_toml_dev_dependencies(backend_dir: str):
        filepath = os.path.join(backend_dir, "pyproject.toml")

        with open(filepath, "r") as f:
            lines = f.readlines()

        count = 0
        for item in BACKEND_DEV_PACKAGES:
            for line in lines[10:]:
                if line.startswith(item):
                    count += 1
                    break

        assert count == len(BACKEND_DEV_PACKAGES)


class TestBackendStaticAssetController:
    @staticmethod
    def test_env_local_exists(project_dir: str):
        filepath = os.path.join(project_dir, ".env.local")

        if not os.path.exists(filepath):
            assert False

    @staticmethod
    def test_backend_dir_valid(backend_dir: str, asset_dir: str):
        setup_filepaths = get_filepaths(os.path.join(asset_dir, "backend")) + [
            "poetry.lock",
            "pyproject.toml",
        ]
        project_filepaths = get_filepaths(backend_dir)

        assert len(setup_filepaths) == len(project_filepaths)
