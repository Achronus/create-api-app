import os
import shutil

from ..conf.constants import VENV_NAME
from .base import ControllerBase


class CleanupController(ControllerBase):
    """A controller for handling project cleanup."""
    def __init__(self) -> None:
        tasks = [
            (self.node_modules, "Removing [green]node_modules[/green]"),
            (self.delete_venv, "Removing [yellow]venv[/yellow]"),
            (self.delete_pycache, "Removing [yellow]pycache[/yellow]")
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

    def delete_pycache(self) -> None:
        """Deletes the virtual environment folder and assets."""
        if os.path.exists(os.path.join(self.project_paths.BACKEND, '__pycache__')):
            shutil.rmtree(os.path.join(self.project_paths.BACKEND, '__pycache__'))
