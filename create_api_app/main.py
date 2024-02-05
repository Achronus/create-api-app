import os
import shutil


from .conf.constants.filepaths import set_project_name, set_db_url
from .conf.helper import set_tw_standalone_filename
from .setup import run_tasks
from .utils.helper import strip_whitespace_and_dashes
from .utils.printables import project_table, project_complete_panel

import typer
from typing_extensions import Annotated
from rich.console import Console


app = typer.Typer(rich_markup_mode="rich")

console = Console()


@app.command()
def main(
        name: Annotated[str, typer.Argument(help="The name of the project", show_default=False)], 
        db_url: Annotated[str, typer.Argument(help="The projects database URL", show_default=True, metavar="DB_URL", rich_help_panel="Secondary Arguments")] = 'sqlite:///./database.db'
    ) -> None:
    """Create a FastAPI and NextJS project with NAME and an optional DB_URL."""
    name = strip_whitespace_and_dashes(name)
    path = os.path.join(os.getcwd(), name)

    # Store arguments as env variables
    set_project_name(name)
    set_db_url(db_url)

    # Provide pretty print formats
    name_print = f'[cyan]{name}[/cyan]'
    path_print = f'[dark_goldenrod]{path}[/dark_goldenrod]'

    console.print(project_table(name, path))

    # Replace project if exists
    if os.path.exists(path):
        typer.confirm("Replace project?", abort=True)

        console.print(f"\nRemoving {name_print} and creating a new one...\n")
        shutil.rmtree(path)
    else:
        console.print(f"\nCreating project {name_print}...\n")

    # Create and move into directory
    os.makedirs(path)
    os.chdir(path)

    # Run task handler
    run_tasks()

    # End of script
    console.print(project_complete_panel())
    console.print(f"Access {name_print} at {path_print}")

    # Provide information for unsupported TailwindCSS standalone CLI
    if set_tw_standalone_filename() == 'unsupported':
        console.print('\nOS not supported for standalone TailwindCSS. [magenta]node_modules[/magenta] kept.')

if __name__ == '__main__':
    app()
