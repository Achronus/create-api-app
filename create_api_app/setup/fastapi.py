import os
import shutil
import subprocess
import textwrap

from .base import ControllerBase
from create_api_app.conf.constants.filepaths import AssetFilenames


class FastAPIFileController(ControllerBase):
    """A FastAPI file creation controller."""

    def __init__(self) -> None:
        tasks = [
            (self.check_db, "Configuring [red]database[/red] files"),
            (self.configure_tests, "Configuring [yellow]test[/yellow] files"),
        ]

        super().__init__(tasks)

        self.root_path = self.project_paths.BACKEND_APP

    def __package_update(self, packages: list[str]) -> None:
        """Helper function for `check_db`. Installed the relevant package, renames the correct `db` folder and removes the unneeded one."""
        new_path = os.path.join(self.root_path, 'db')
        old_path = f'{new_path}_{get_db_type()}'

        os.rename(old_path, new_path)

        # Cleanup db folders
        for folder in os.listdir(self.root_path):
            rm_path = os.path.join(self.root_path, folder)
            
            if folder.startswith('db_'):
                shutil.rmtree(rm_path)

        # Install correct packages
        os.chdir(self.project_paths.BACKEND)

        subprocess.run(["poetry", "add", *packages], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        os.chdir(self.project_paths.ROOT)

    def check_db(self) -> None:
        """Configures the correct backend database."""
        if get_db_type() == 'mongo':
           self.__package_update(MONGO_PACKAGES)
           os.remove(os.path.join(self.root_path, AssetFilenames.DEPENDENCIES))
           os.remove(os.path.join(self.root_path, AssetFilenames.MAIN_SQL))

           os.rename(
               os.path.join(self.root_path, AssetFilenames.MAIN_MONGO), 
               os.path.join(self.root_path, AssetFilenames.MAIN)
            )
        else:
            self.__package_update(SQL_PACKAGES)
            os.remove(os.path.join(self.root_path, AssetFilenames.MAIN_MONGO))
            
            os.rename(
               os.path.join(self.root_path, AssetFilenames.MAIN_SQL), 
               os.path.join(self.root_path, AssetFilenames.MAIN)
            )


    def configure_tests(self) -> None:
        """Adds a `pytest.ini` file to the backend directory."""
        with open(self.project_paths.PYTEST_INI, 'w') as file:
            file.write(textwrap.dedent("""
            [pytest]
            env_files =
                .env.local
                .env

            addopts = -v -s
            """)[1:])
