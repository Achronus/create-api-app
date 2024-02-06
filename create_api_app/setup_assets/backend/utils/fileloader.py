from dataclasses import dataclass
from dotenv import load_dotenv
import os


@dataclass
class DirPaths:
    ROOT: str
    FRONTEND: str
    BACKEND: str
    PUBLIC: str
    STYLES: str


@dataclass
class FilePaths:
    ENV_PROD: str
    ENV_LOCAL: str


class FileLoader:
    """A class for loading files."""
    def __init__(self) -> None:
        self.DIRPATHS = DirPaths(
            os.getcwd(), 
            *self.finder([
            'frontend', 
            'backend', 
            'public',
            'styles'
            ], self.is_dir)
        )
        self.FILEPATHS = FilePaths(
            *self.finder([
                '.env.prod',
                '.env.local'
            ], self.is_file)
        )

        self.local_dotenv()
        self.prod_dotenv()

    @staticmethod
    def finder(targets: list[str], condition_func: str) -> list[str]:
        """Finds target files or directories in the current working directory."""
        output = []
        for root, dirs, files in os.walk(os.getcwd()):
            for target in targets:
                if condition_func(target, files, dirs):
                    output.append(os.path.join(root, target))
        return output

    @staticmethod
    def is_file(target: str, files: str, dirs: str) -> str:
        """Searches for a file with the given name in the current working directory."""
        return target in files

    @staticmethod
    def is_dir(target: str, files: str, dirs: str) -> str:
        """Searches for a list of directory names in the current working directory."""
        return target in dirs
    
    def prod_dotenv(self) -> None:
        """Loads the production dotenv file."""
        load_dotenv(self.FILEPATHS.ENV_PROD)

    def local_dotenv(self) -> None:
        """Loads the local dotenv file."""
        load_dotenv(self.FILEPATHS.ENV_LOCAL)
