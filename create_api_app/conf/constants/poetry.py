from .filepaths import AssetFilenames


class PoetryContent:
    """A helper class for retrieving content for the Poetry installation."""

    def __init__(self) -> None:
        self.START_SERVER_CMD = f"{AssetFilenames.BUILD.split('.')[0]}:start"

        self.start_desc = '"""Start the server."""'
        self.BUILD_FILE_CONTENT = f"""
        import argparse

        from app.config.settings import settings

        import uvicorn


        def start(env_mode: str) -> None:
            {self.start_desc}
            reload_check = True if env_mode == 'dev' else False

            uvicorn.run(
                "app.main:app", 
                host=settings.HOST, 
                port=settings.PORT, 
                reload=reload_check 
        )


        if __name__ == "__main__":
            parser = argparse.ArgumentParser(description='Start the server.')
            parser.add_argument('-e', '--env', type=str, default='dev', choices=['dev', 'prod'], required=True)

            args = parser.parse_args()
            start(args.env)
        """

    def pyproject_desc(self) -> str:
        return 'description = "A FastAPI backend for processing API data and passing it to the frontend."'

    def pyproject_author(self) -> str:
        return "rpartridge101@gmail.com"

    def pyproject_scripts(self) -> str:
        return f'\n\n[tool.poetry.scripts]\nrun = "{self.START_SERVER_CMD}"\n\n'
