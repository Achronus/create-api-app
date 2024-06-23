import os
import shutil

from create_api_app.setup.nextjs import NextJSController
from create_api_app.setup.backend import VEnvController, BackendStaticAssetController

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


BACKEND_TASKS = [
    (VEnvController, "Creating [yellow]Poetry[/yellow] project..."),
    (
        BackendStaticAssetController,
        "Adding core [cyan]backend[/cyan] assets...",
    ),
]


def handle_existing(name: str) -> None:
    name = typer.style(f"'{name}'", fg=typer.colors.MAGENTA)
    exists = typer.style("exists", fg=typer.colors.RED)
    overwrite = typer.style("overwrite", fg=typer.colors.YELLOW)

    delete = typer.confirm(
        f"A project with the name {name} already {exists}! Do you want to {overwrite} it?"
    )

    if not delete:
        console.print("\n[dark_goldenrod]No changes made.[/dark_goldenrod]")
        raise typer.Abort()


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
        handle_existing(name)
        console.print(f"\nRemoving {name_print} and creating a new one...\n")
        shutil.rmtree(path)
    else:
        console.print(f"\nCreating project {name_print}...")

    # Create and move into directory
    os.makedirs(path)
    os.chdir(path)

    # Run application
    console.print("  Steps to complete:")
    console.print("    1. [yellow]Backend creation[/yellow]")
    console.print("    2. [green]Frontend creation[/green]")
    console.print("    3. [cyan]File cleanup[/cyan]\n")

    console.print("Performing step: [yellow]1[/yellow]/[cyan]3[/cyan]\n")
    run_tasks(
        tasks=BACKEND_TASKS,
        console=console,
    )

    console.print("\nPerforming step: [green]2[/green]/[cyan]3[/cyan]")

    # End of script
    console.print(project_complete_panel())
    console.print(
        f"Access the project files here [link={os.getcwd()}]{name_print}[/link]\n"
    )


if __name__ == "__main__":
    app()
