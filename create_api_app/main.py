import os
import shutil

from .conf.constants.filepaths import set_project_name, set_db_type
from .setup import run_tasks
from .utils.helper import strip_whitespace_and_dashes
from .utils.printables import project_table, project_complete_panel

import typer
from typing_extensions import Annotated
from rich.console import Console


app = typer.Typer(rich_markup_mode="rich")

console = Console()


def db_type_choices(value: str) -> str:
    """Callback function for the `db_type` parameter in `main()`."""
    valid_choices = ['sql', 'mongo']

    if value not in valid_choices:
        raise typer.BadParameter(f"Invalid choice: '{value}'. Valid choices are: [{', '.join(valid_choices)}].")
    return value


@app.command()
def main(
        name: Annotated[str, typer.Argument(
            help="The name of the project", 
            show_default=False
        )], 
        db_type: Annotated[str, typer.Argument(
            help="The projects database type. Options ['sql', 'mongo']", 
            show_default=True, 
            metavar="DB_TYPE", 
            rich_help_panel="Secondary Arguments", 
            callback=db_type_choices
        )] = 'sql'
    ) -> None:
    """Create a FastAPI and NextJS project with NAME and an optional DB_URL."""
    name = strip_whitespace_and_dashes(name)
    path = os.path.join(os.getcwd(), name)

    # Store arguments as env variables
    set_project_name(name)
    set_db_type(db_type.lower())

    # Provide pretty print formats
    name_print = f'[purple]{name}[/purple]'
    access_print = '[dark_goldenrod]docker cp creating_project:/app/<project_name> <path>/<project_name>[/dark_goldenrod]'

    console.print(project_table(name, db_type))

    # Replace project if exists
    if os.path.exists(path):
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
    console.print(f"Access {name_print} with {access_print}")


if __name__ == '__main__':
    app()
