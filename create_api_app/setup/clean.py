import os
import shutil
import subprocess

from ..conf.constants import VENV_NAME
from .base import ControllerBase


class CleanupController(ControllerBase):
    """A controller for handling project cleanup."""
    def __init__(self) -> None:
        tasks = [
            (self.node_modules, "Removing [magenta]node_modules[/magenta]"),
            (self.delete_venv, "Removing [yellow]venv[/yellow]"),
            (self.poetry_install, "Finalising project")
        ]

        super().__init__(tasks)
    
    def node_modules(self) -> None:
        """Removes the `node_modules` folder from frontend (if exists)."""
        # If exists, remove node_modules
        if (os.path.join(self.project_paths.FRONTEND, 'node_modules')):
            shutil.rmtree(os.path.join(self.project_paths.FRONTEND, 'node_modules'))

    def delete_venv(self) -> None:
        """Deletes the virtual environment folder and assets."""
        shutil.rmtree(os.path.join(self.project_paths.ROOT, VENV_NAME))

    def poetry_install(self) -> None:
        """Finalise the application with a poetry install."""
        os.chdir(self.project_paths.BACKEND)

        subprocess.run(["poetry", "shell"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.run(["poetry", "install"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        os.chdir(self.project_paths.ROOT)
