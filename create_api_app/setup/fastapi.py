import os
import shutil
import textwrap
import subprocess

from .base import ControllerBase
from ..conf.constants.fastapi import FastAPIDirPaths, FastAPIContent
from ..conf.constants.filepaths import get_db_url
from ..conf.constants.poetry import PoetryCommands, PoetryContent
from ..conf.file_handler import insert_into_file


class FastAPIFileController(ControllerBase):
    """A FastAPI file creation controller."""
    def __init__(self) -> None:
        tasks = [
            (self.check_db, "Configuring [red]database[/red] files"),
            (self.create_build, "Creating [yellow]build[/yellow] file")
        ]

        super().__init__(tasks)

        self.poetry_commands = PoetryCommands()
        self.poetry_content = PoetryContent()

        self.dir_paths = FastAPIDirPaths()

    def __package_update(self, package_name: str, db_type: str) -> None:
        """Helper function for `check_db`. Installed the relevant package, renames the correct `db` folder and removes the unneeded one."""
        root_path = self.project_paths.BACKEND
        new_path = os.path.join(root_path, 'db')
        old_path = f'{new_path}_{db_type}'

        os.rename(old_path, new_path)

        # Cleanup db folders
        for folder in os.listdir(root_path):
            rm_path = os.path.join(root_path, folder)
            
            if folder.startswith('db_'):
                shutil.rmtree(rm_path)

        # Install correct package
        subprocess.run(["poetry", "add", package_name], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def check_db(self) -> None:
        """Configures the correct backend database."""
        db_url = get_db_url().split('://')[0]

        if 'mongo' in db_url:
           self.__package_update("beanie", "mongo")
           os.remove(os.path.join(self.project_paths.BACKEND, 'dependencies.py'))
        else:
            self.__package_update("sqlalchemy", "sql")

            if db_url == 'sqlite':
                insert_into_file(
                    FastAPIContent.SQLITE_DB_POSITION, 
                    FastAPIContent.SQLITE_DB_CONTENT, 
                    self.dir_paths.DATABASE_INIT_FILE
                )

    def create_build(self) -> None:
        """Creates a build file in the root directory for watching TailwindCSS."""
        content = textwrap.dedent(self.poetry_content.BUILD_FILE_CONTENT)[1:]

        with open(self.project_paths.PROJECT_BUILD, 'w') as file:
            file.write(content)
