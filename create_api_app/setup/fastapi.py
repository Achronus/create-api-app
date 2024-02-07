import os
import shutil
import subprocess

from .base import ControllerBase
from ..conf.constants.fastapi import FastAPIDirPaths, FastAPIContent
from ..conf.constants.filepaths import get_db_url
from ..conf.file_handler import insert_into_file


class FastAPIFileController(ControllerBase):
    """A FastAPI file creation controller."""
    def __init__(self) -> None:
        tasks = [
            (self.check_db, "Configuring [red]database[/red] files"),
            (self.configure_tests, "Configuring [yellow]test[/yellow] files")
        ]

        super().__init__(tasks)

        self.dir_paths = FastAPIDirPaths()
        self.root_path = self.project_paths.BACKEND_APP

    def __package_update(self, package_name: str, db_type: str) -> None:
        """Helper function for `check_db`. Installed the relevant package, renames the correct `db` folder and removes the unneeded one."""
        new_path = os.path.join(self.root_path, 'db')
        old_path = f'{new_path}_{db_type}'

        os.rename(old_path, new_path)

        # Cleanup db folders
        for folder in os.listdir(self.root_path):
            rm_path = os.path.join(self.root_path, folder)
            
            if folder.startswith('db_'):
                shutil.rmtree(rm_path)

        # Install correct packages
        os.chdir(self.project_paths.BACKEND)

        subprocess.run(["poetry", "add", package_name], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        os.chdir(self.project_paths.ROOT)

    def check_db(self) -> None:
        """Configures the correct backend database."""
        db_url = get_db_url().split('://')[0]

        if 'mongo' in db_url:
           self.__package_update("beanie", "mongo")
           os.remove(os.path.join(self.root_path, 'dependencies.py'))
        else:
            self.__package_update("sqlalchemy", "sql")

            if db_url == 'sqlite':
                insert_into_file(
                    FastAPIContent.SQLITE_DB_POSITION, 
                    FastAPIContent.SQLITE_DB_CONTENT, 
                    self.dir_paths.DATABASE_INIT_FILE
                )

    def configure_tests(self) -> None:
        """Adds a `pytest.ini` file to the backend directory."""
        with open(self.project_paths.PYTEST_INI, 'w') as file:
            file.write(FastAPIContent.PYTEST_INI)
