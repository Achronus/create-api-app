import os
import shutil
import subprocess

from create_api_app.conf.constants import PACKAGES
from create_api_app.conf.constants.content import EnvFileContent, FrontendContent
from create_api_app.conf.constants.filepaths import (
    ProjectPaths,
    SetupAssetsDirNames,
    SetupDirPaths,
)
from create_api_app.conf.file_handler import append_to_file, replace_content
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


class FrontendStaticAssetController(ControllerBase):
    """A controller for managing the frontend static assets."""

    def __init__(self, project_paths: ProjectPaths = None) -> None:
        tasks = [
            (
                self.add_folders,
                "Updating [green]project[/green] structure",
            ),
            (
                self.update_files,
                "Updating [green]core[/green] files and adding [green]new[/green] ones",
            ),
            (
                self.update_env,
                "Updating [yellow].env.local[/yellow] API keys",
            ),
        ]

        for package in PACKAGES.items:
            if package.name == "uploadthing" and not package.exclude:
                tasks.append(
                    (
                        self.add_uploadthing,
                        "Adding [red]uploadthing[/red] files",
                    ),
                )

        super().__init__(tasks, project_paths)

        self.content = FrontendContent()

        self.src_path = os.path.join(os.getcwd(), SetupAssetsDirNames.FRONTEND, "src")
        self.frontend_path = os.path.join(os.getcwd(), SetupAssetsDirNames.FRONTEND)

    def add_folders(self) -> None:
        """Add empty folders to the frontend."""
        dir_paths = [
            os.path.join(self.src_path, "components"),
            os.path.join(self.src_path, "data"),
            os.path.join(self.src_path, "hooks"),
            os.path.join(self.src_path, "layouts"),
            os.path.join(self.src_path, "pages"),
            os.path.join(self.src_path, "types"),
        ]

        for directory in dir_paths:
            os.makedirs(directory, exist_ok=True)

    def update_files(self) -> None:
        """Replaces frontend files with new ones."""
        shutil.copytree(
            SetupDirPaths.FRONTEND_ASSETS, self.frontend_path, dirs_exist_ok=True
        )

        replace_content(
            old="extend: {",
            new=self.content.tailwind_font(),
            path=self.project_paths.TAILWIND_CONF,
        )

        replace_content(
            old="new-york",
            new="default",
            path=self.project_paths.SHAD_CONF,
        )

    def update_env(self) -> None:
        """Adds API keys to `.env.local` based on `exclude` command parameter."""
        env_generator = EnvFileContent(PACKAGES)

        extra_content = "\n" + env_generator.make()

        append_to_file(extra_content, self.project_paths.ENV_LOCAL)

    def add_uploadthing(self) -> None:
        """Adds `uploadthing` files to the project."""
        shutil.copytree(
            SetupDirPaths.UPLOADTHING_ASSETS,
            self.project_paths.FRONTEND,
            dirs_exist_ok=True,
        )
