import os

from .base import ControllerBase


class CleanupController(ControllerBase):
    """A controller for handling project cleanup."""

    def __init__(self) -> None:
        tasks = [
            (self.clean_backend, "Tidying [yellow]backend[/yellow]"),
            (self.clean_frontend, "Tidying [green]frontend[/green]"),
        ]

        super().__init__(tasks)

    def clean_backend(self) -> None:
        """Removes files from the backend."""
        pass

    def clean_frontend(self) -> None:
        """Removes files from the frontend."""
        files = [
            os.path.join(self.project_paths.FRONTEND, ".gitignore"),
            os.path.join(self.project_paths.FRONTEND, "bun.lockb"),
            os.path.join(self.project_paths.FRONTEND, "README.md"),
        ]

        for file in files:
            os.remove(file)

        public_dir = os.path.join(self.project_paths.FRONTEND, "public")
        for file in os.listdir(public_dir):
            os.remove(os.path.join(public_dir, file))
