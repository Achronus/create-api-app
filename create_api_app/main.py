import os
import shutil

from .conf.constants.filepaths import set_project_name
from .setup import run_tasks
from .utils.helper import strip_whitespace_and_dashes
from .utils.printables import project_table, project_complete_panel

import docker
import typer
from typing_extensions import Annotated
from rich.console import Console


app = typer.Typer(rich_markup_mode="rich")

console = Console()


def check_docker_running(console: Console) -> None:
    try:
        client = docker.from_env()
        client.version()
    except docker.errors.DockerException:
        console.print(
            "[red]Error[/red]: please start the [cyan]Docker Engine[/cyan] first!"
        )
        raise typer.Abort()


@app.command()
def main(
    name: Annotated[
        str, typer.Argument(help="The name of the project", show_default=False)
    ],
) -> None:
    """Create a FastAPI and NextJS project with NAME and an optional DB_URL."""
    check_docker_running(console)

    name = strip_whitespace_and_dashes(name)
    path = os.path.join(os.getcwd(), name)

    # Store arguments as env variables
    set_project_name(name)

    # Provide pretty print formats
    name_print = f"[magenta]{name}[/magenta]"
    access_print = f"[dark_goldenrod]docker cp creating_project:/app/{name} {os.path.join(os.getcwd(), name)}[/dark_goldenrod]"

    console.print(project_table(name, "MongoDB"))

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


if __name__ == "__main__":
    app()
