import os
import shutil
import textwrap

from create_api_app.conf.constants import BACKEND_ENV_VARIABLES
from create_api_app.conf.constants.docker import DockerContent
from create_api_app.conf.constants.filepaths import (
    AssetFilenames,
    SetupDirPaths,
    ProjectPaths,
)
from create_api_app.conf.constants.poetry import PoetryContent
from .base import ControllerBase


class StaticAssetsController(ControllerBase):
    """A controller for handling the static assets."""

    def __init__(self) -> None:
        tasks = [
            (
                self.move_setup_assets,
                "Setting up [green]frontend[/green] and [yellow]backend[/yellow] files",
            ),
            (self.create_dotenv, "Building [magenta].env[/magenta] files"),
            (self.create_build, "Creating backend [yellow]build[/yellow] file"),
        ]

        super().__init__(tasks)

        self.poetry_content = PoetryContent()
        self.project_paths = ProjectPaths()

    def create_dotenv(self) -> None:
        """Creates a `.env` file in the root for docker specific config and another in the backend folder. Adds items to them both."""
        docker_content = DockerContent()
        docker_path = os.path.join(self.project_paths.ROOT, AssetFilenames.PROD_ENV)
        backend_path = os.path.join(
            self.project_paths.BACKEND, AssetFilenames.LOCAL_ENV
        )

        with open(docker_path, "w") as file:
            file.write(docker_content.env_config())

        with open(backend_path, "w") as file:
            file.write("\n".join(BACKEND_ENV_VARIABLES))

        # Update frontend .env.example -> .env.local
        frontend_env = os.path.join(self.project_paths.FRONTEND, ".env.example")
        os.rename(frontend_env, os.path.join(self.project_paths.FRONTEND, ".env.local"))

    def move_setup_assets(self) -> None:
        """Moves the items in the `setup_assets` folder into the project directory."""
        shutil.copytree(SetupDirPaths.ASSETS, os.getcwd(), dirs_exist_ok=True)

    def create_build(self) -> None:
        """Creates a build file in the root directory for starting the backend server."""
        content = textwrap.dedent(self.poetry_content.BUILD_FILE_CONTENT)[1:]

        with open(self.project_paths.BACKEND_BUILD, "w") as file:
            file.write(content)
