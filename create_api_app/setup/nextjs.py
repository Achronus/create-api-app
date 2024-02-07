import os
import subprocess

from .base import ControllerBase
from ..conf.constants import NPM_PACKAGES


class NextJSController(ControllerBase):
    """A NextJS file creation controller."""
    def __init__(self) -> None:
        tasks = [
            (self.update_npm, "Adding [red]NPM[/red] packages")
        ]

        super().__init__(tasks)


    def update_npm(self) -> None:
        """Adds the remaining required packages to the `package.json`."""
        os.chdir(self.project_paths.FRONTEND)

        subprocess.run(["bun", "add", *NPM_PACKAGES], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.run(["bun", "update", "-f"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        os.chdir(self.project_paths.ROOT)
