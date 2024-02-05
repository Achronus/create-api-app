import os
import shutil

from ..conf.constants.docker import DockerContent
from ..conf.constants.filepaths import (
    AssetFilenames, 
    SetupDirPaths, 
    ProjectPaths, 
    get_db_url
)
from .base import ControllerBase


class StaticAssetsController(ControllerBase):
    """A controller for handling the static assets."""
    def __init__(self) -> None:
        tasks = [
            (self.move_setup_assets, "Creating [green]static files[/green] and [green]templates[/green]"),
            (self.create_dotenv, "Building [magenta].env[/magenta] files")
        ]

        super().__init__(tasks)

        self.project_paths = ProjectPaths()

    def create_dotenv(self) -> None:
        """Creates a `.env` file in the root for docker specific config and another in the backend folder. Adds items to them both."""
        docker_content = DockerContent()
        docker_path = os.path.join(os.path.dirname(os.getcwd()), AssetFilenames.PROD_ENV)
        backend_path = os.path.join(self.project_paths.BACKEND, AssetFilenames.LOCAL_ENV)

        with open(docker_path, "w") as file:
            file.write(docker_content.env_config())

        with open(backend_path, "w") as file:
            file.write(f'DATABASE_URL={get_db_url()}')

    def move_setup_assets(self) -> None:
        """Moves the items in the `setup_assets` folder into the project directory."""
        # Move assets into root project dir
        shutil.copytree(SetupDirPaths.ASSETS, os.getcwd(), dirs_exist_ok=True)

        # Move .gitignore, if available
        gitignore_path = os.path.join(os.getcwd(), '.gitignore')
        if gitignore_path:
            shutil.copy(gitignore_path, os.path.dirname(os.getcwd()))
            os.remove(gitignore_path)
