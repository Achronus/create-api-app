class PoetryContent:
    """A helper class for retrieving content for the Poetry installation."""

    def __init__(self) -> None:
        self.start_server_cmd = "app-start"
        self.start_server_location = "app.start:run"

    def pyproject_desc(self) -> str:
        return 'description = "A FastAPI backend for processing API data and passing it to the frontend."'

    def pyproject_author(self) -> str:
        return "rpartridge101@gmail.com"

    def pyproject_scripts(self) -> str:
        return f'\n\n[tool.poetry.scripts]\n{self.start_server_cmd} = "{self.start_server_location}"\n\n'


class FrontendContent:
    """A helper class for retrieving content for the frontend installation."""

    def tailwind_font(self) -> str:
        """New content for the `Rubik` font in the tailwind config."""
        return "\n".join(
            [
                "extend: {",
                "      fontFamily: {",
                '        rubik: ["Rubik", "sans-serif"],',
                "      },",
            ]
        )
