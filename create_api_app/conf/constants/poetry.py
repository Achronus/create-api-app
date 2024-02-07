from .filepaths import AssetFilenames


# Define Poetry script commands
class PoetryCommands:
    def __init__(self) -> None:
        self.START_SERVER_CMD = f"{AssetFilenames.BUILD.split('.')[0]}:start"

# Define Poetry script content
# Specific to setup/venv.py -> init_project()
class PoetryContent:
    def __init__(self) -> None:
        self.commands = PoetryCommands()

        self.SCRIPT_INSERT_LOC = 'readme = "README.md"'
        self.SCRIPT_CONTENT = '\n'.join([
            "[tool.poetry.scripts]",
            f'run = "{self.commands.START_SERVER_CMD}"'
        ])

        self.start_desc = '"""Start the server."""'
        self.BUILD_FILE_CONTENT = f"""
        import os

        from app.config.settings import settings

        import uvicorn


        def start() -> None:
            {self.start_desc}
            reload_check = True if os.getenv('ENV_TYPE') == 'dev' else False

            uvicorn.run(
                "app.main:app", 
                host=settings.HOST, 
                port=settings.PORT, 
                reload=reload_check 
        )


        if __name__ == "__main__":
            start()
        """
