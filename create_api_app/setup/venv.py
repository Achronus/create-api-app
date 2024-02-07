import re
import os
import subprocess
import sys

from ..conf.constants import VENV_NAME, CORE_BACKEND_PACKAGES, BACKEND_DEV_PACKAGES
from ..conf.constants.filepaths import get_project_name, set_poetry_version
from ..conf.constants.poetry import PoetryContent
from ..conf.file_handler import insert_into_file
from .base import ControllerBase


class VEnvController(ControllerBase):
    """A controller for creating a Python virtual environment."""
    def __init__(self) -> None:
        tasks = [
            (self.create, "Building [yellow]venv[/yellow]"),
            (self.update_pip, "Updating [yellow]PIP[/yellow]"),
            (self.install, "Installing [yellow]PIP[/yellow] packages"),
            (self.init_project, f"Initalising [cyan]{get_project_name()}[/cyan] as [green]Poetry[/green] project"),
            (self.add_dependencies, "Adding [yellow]PIP[/yellow] packages to [green]Poetry[/green]")
        ]

        super().__init__(tasks)

        self.poetry_content = PoetryContent()
        VENV_LOCATION = os.path.join(os.getcwd(), VENV_NAME)

        if sys.platform.startswith("win"):
            self.venv = f"{VENV_LOCATION}\\Scripts"
        else:
            self.venv = f"source {VENV_LOCATION}/bin/"

    @staticmethod
    def create() -> None:
        """Creates a new virtual environment."""
        subprocess.run(["python", "-m", "venv", VENV_NAME], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def update_pip(self) -> None:
        """Updates `PIP` to the latest version."""
        subprocess.run([os.path.join(self.venv, "pip"), "install", "--upgrade", "pip"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def install(self) -> None:
        """Installs a set of `PIP` packages."""
        subprocess.run([os.path.join(self.venv, "pip"), "install", "poetry", *CORE_BACKEND_PACKAGES], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def init_project(self) -> None:
        """Creates a poetry project."""
        # Create Poetry project
        subprocess.run(["poetry", "new", "app"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

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
        subprocess.run(["poetry", "shell"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        subprocess.run(["poetry", "add", *CORE_BACKEND_PACKAGES], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        subprocess.run(["poetry", "add", *BACKEND_DEV_PACKAGES, '--dev'], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Store poetry version
        pv_result = subprocess.run(["poetry", "--version"], capture_output=True, text=True)
        set_poetry_version(re.search(r'\d+\.\d+\.\d+', pv_result.stdout).group(0))

        os.chdir(self.project_paths.ROOT)
