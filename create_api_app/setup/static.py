import os
import shutil

from create_api_app.conf.constants.filepaths import (
    SetupDirPaths,
    ProjectPaths,
)
from .base import ControllerBase


class StaticAssetsController(ControllerBase):
    """A controller for handling the static assets."""

    def __init__(self, project_paths: ProjectPaths = None) -> None:
        tasks = [
            (
                self.move_setup_assets,
                "Setting up [green]frontend[/green] and [yellow]backend[/yellow] files",
            ),
        ]

        super().__init__(tasks, project_paths)

    def move_setup_assets(self) -> None:
        """Moves the items in the `setup_assets` folder into the project directory."""
        shutil.copytree(SetupDirPaths.ASSETS, os.getcwd(), dirs_exist_ok=True)
