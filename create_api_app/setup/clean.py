import json
import os

from typing import Callable

from create_api_app.conf.constants import PACKAGES
from create_api_app.conf.constants.content import FrontendContent
from create_api_app.conf.storage import Package

from .base import ControllerBase
from create_api_app.conf.constants.filepaths import ProjectPaths


class CleanupController(ControllerBase):
    """A controller for handling project cleanup."""

    def __init__(self) -> None:
        tasks = [
            (self.clean_backend, "Tidying [yellow]backend[/yellow]"),
            (self.clean_frontend, "Tidying [green]frontend[/green]"),
        ]

        if PACKAGES.exclusions():
            handler = PackageHandler(PACKAGES.exclusions())
            tasks.append(handler.get_task())

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


class PackageHandler:
    """Handles the logic for removing packages."""

    def __init__(self, packages: list[Package]) -> None:
        self.packages = packages

        self.project_paths = ProjectPaths()
        self.env_file = self.project_paths.ENV_LOCAL

        with open(self.project_paths.PACKAGE_JSON, "r") as f:
            content = f.read()
            self.package_json_content = json.loads(content)

    def get_task(self) -> tuple[Callable, str]:
        """Gets the package handler task."""
        names = ", ".join([package.name_str() for package in self.packages])

        return (
            self.remove_packages,
            f"Removing {names} dependencies",
        )

    def remove_packages(self) -> None:
        """Removes dependencies from `package.json` and other content from files if required."""
        exclude = []
        for package in self.packages:
            if package.name == "uploadthing":
                handler = RemotePatternHandler(self.project_paths)
                handler.update_file()

            exclude.extend(package.dependencies)

        new_content = self.package_json_content
        for package in exclude:
            new_content["dependencies"].pop(package)

        new_content = json.dumps(new_content, indent=2)

        with open(self.project_paths.PACKAGE_JSON, "w") as f:
            f.write(new_content)


class RemotePatternHandler:
    """Handles the logic for removing the `uploadthing` `remotePattern` from `next.config.mjs`."""

    def __init__(self, paths: ProjectPaths) -> None:
        self.conf = paths.NEXT_CONF

        with open(self.conf, "r") as file:
            self.content = file.readlines()

    def get_new_content(self) -> list[str]:
        """Removes the required information from the file."""
        new_content = self.content.copy()
        in_patterns = False

        for line in self.content:
            if line.strip().startswith("remotePatterns"):
                in_patterns = True

            if in_patterns:
                for item in FrontendContent.ut_remote_pattern():
                    new_content.remove(item)
                break

        return new_content

    def update_file(self) -> None:
        """Updates the content file with the new content."""
        new_content = self.get_new_content()

        with open(self.conf, "w") as f:
            f.writelines(new_content)
