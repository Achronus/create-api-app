import re
import os
import subprocess

from ..conf.constants import CORE_BACKEND_PACKAGES, BACKEND_DEV_PACKAGES
from ..conf.constants.filepaths import set_poetry_version
from ..conf.constants.poetry import PoetryContent
from ..conf.file_handler import insert_into_file
from .base import ControllerBase


class VEnvController(ControllerBase):
    """A controller for creating a Python virtual environment."""
    def __init__(self) -> None:
        tasks = [
            (self.install, "Installing [yellow]PIP[/yellow] packages"),
            (self.init_project, "Initalising [yellow]backend[/yellow] as [green]Poetry[/green] project"),
            (self.add_dependencies, "Adding [yellow]PIP[/yellow] packages to [green]Poetry[/green]")
        ]

        super().__init__(tasks)

        self.poetry_content = PoetryContent()

    def install(self) -> None:
        """Installs a set of `PIP` packages."""
        subprocess.run(["pip", "install", "poetry", *CORE_BACKEND_PACKAGES], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def init_project(self) -> None:
        """Creates a poetry project."""
        # Create Poetry project
        subprocess.run(["poetry", "new", "app"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        os.rename(os.path.join(self.project_paths.ROOT, 'app'), 'backend')
        os.chdir(self.project_paths.BACKEND)

        # Add scripts to pyproject.toml
        insert_into_file(
            self.poetry_content.SCRIPT_INSERT_LOC, 
            f'\n\n{self.poetry_content.SCRIPT_CONTENT}', 
            self.project_paths.POETRY_CONF
        )

    def add_dependencies(self) -> None:
        """Adds PIP packages to the poetry project."""
        subprocess.run(["poetry", "add", *CORE_BACKEND_PACKAGES], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        subprocess.run(["poetry", "add", *BACKEND_DEV_PACKAGES, '--dev'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Store poetry version
        pv_result = subprocess.run(["poetry", "--version"], capture_output=True, text=True)
        set_poetry_version(re.search(r'\d+\.\d+\.\d+', pv_result.stdout).group(0))

        os.chdir(self.project_paths.ROOT)
