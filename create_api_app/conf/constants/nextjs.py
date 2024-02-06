import subprocess

from .filepaths import get_project_name
from . import NPM_PACKAGES


class NextJSContent:
    def __init__(self) -> None:
        self.FLAGS = [
            "--ts",
            "--tailwind",
            "--eslint",
            "--no-app",
            "--src-dir",
            "--import-alias '@/*'",
            "--use-bun"
        ]

    @staticmethod
    def __get_package_version(package_name: str) -> str:
        """A helper function for retrieving a single package version."""
        result = subprocess.run(["npx", "view", package_name, "version"], shell=True, capture_output=True, text=True)
        return result.stdout.strip()

    def package_json(self) -> dict[str, str]:
        """Creates the package json content and returns its as a dictionary."""
        core_deps = {pkg: self.__get_package_version(pkg) for pkg in NPM_PACKAGES}

        return {
            "name": f"{get_project_name()}",
            "version": "0.1.0",
            "private": True,
            "scripts": {
                "dev": "next dev",
                "build": "next build",
                "start": "next start",
                "lint": "next lint"
            },
            "dependencies": core_deps,
        }
