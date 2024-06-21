import os
import shutil
import subprocess

from create_api_app.conf.constants.filepaths import ProjectPaths
from .base import ControllerBase


class NextJSController(ControllerBase):
    """A controller for creating the Next.js assets."""

    def __init__(self, project_paths: ProjectPaths = None) -> None:
        tasks = [
            (
                self.install,
                "Creating [green]Next.js[/green] project",
            ),
        ]

        super().__init__(tasks, project_paths)

    def install(self) -> None:
        """Creates the Next.js files."""
        subprocess.run(["build-nextjs-app", "frontend"])
