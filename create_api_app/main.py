import os
import shutil
import textwrap
import time
from typing import Optional

from create_api_app.conf.constants import ExcludeOptions, PACKAGES
from create_api_app.setup.clean import CleanupController
from create_api_app.setup.frontend import (
    FrontendStaticAssetController,
    NextJSController,
)
from create_api_app.setup.backend import VEnvController, BackendStaticAssetController

from create_api_app.conf.constants.filepaths import (
    ProjectPaths,
    set_exclude_value,
    set_project_name,
)
from .setup import run_frontend_tasks, run_tasks
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
        "Adding core [yellow]backend[/yellow] assets...",
    ),
]

FRONTEND_TASKS = [
    (FrontendStaticAssetController, "Updating [green]frontend[/green] assets..."),
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


def check_project_deleted(path: str) -> None:
    deleted = False

    while not deleted:
        if not os.path.exists(path):
            deleted = True

    time.sleep(5)


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
    exclude: Annotated[
        Optional[ExcludeOptions],
        typer.Argument(
            help="Exclude packages from the install. Accepts a combination of: (c)lerk, (u)ploadthing, (s)tripe",
        ),
    ] = None,
) -> None:
    """Create a FastAPI and NextJS project with NAME and an optional DB_URL."""
    check_docker_running(console)

    name = strip_whitespace_and_dashes(name)
    path = os.path.join(os.getcwd(), name)

    # Store arguments as env variables
    set_project_name(name)
    set_exclude_value(exclude if exclude else "")

    # Update packages
    PACKAGES.update(exclude)

    # Provide pretty print formats
    name_print = f"[magenta]{name}[/magenta]"

    console.print(project_table(name, "MongoDB"))

    try:
        # Replace project if exists
        if os.path.exists(path):
            handle_existing(name)
            console.print(f"\nRemoving {name_print} and creating a new one...\n")
            shutil.rmtree(path)
            check_project_deleted(path)
        else:
            console.print(f"\nCreating project {name_print}...")

        # Create and move into directory
        os.makedirs(path)
        os.chdir(path)
    except Exception as e:
        console.print(f"Something went wrong:\n  {e}")
        raise typer.Abort()

    # Run application
    console.print("  Stages to complete:")
    console.print("    1. [yellow]Backend creation[/yellow]")
    console.print("    2. [green]Frontend creation[/green]")
    console.print("    3. [cyan]File cleanup[/cyan]\n")

    console.print("Performing stage: [yellow]1[/yellow]/[cyan]3[/cyan]\n")
    run_tasks(
        tasks=BACKEND_TASKS,
        console=console,
    )

    console.print("\nPerforming stage: [green]2[/green]/[cyan]3[/cyan]")
    run_frontend_tasks(
        container_controller=NextJSController(),
        other_tasks=FRONTEND_TASKS,
        console=console,
    )

    console.print("\nPerforming stage: [cyan]3[/cyan]/[cyan]3[/cyan]")
    run_tasks(
        tasks=[(CleanupController, "Cleaning project...")],
        console=console,
    )

    # End of script
    console.print(project_complete_panel())
    console.print(
        f"Access the project files here [link={os.getcwd()}]{name_print}[/link]"
    )

    project_paths = ProjectPaths(name)
    console.print(
        textwrap.dedent(f"""
    [dark_goldenrod]Not sure where to start?[/dark_goldenrod]
      [cyan]Core[/cyan]
        - [magenta][link={project_paths.ENV_LOCAL}].env.local[/link][/magenta] - Update your API keys

      [cyan]Backend[/cyan]
        - [yellow][link={project_paths.SETTINGS}]config/settings.py[/link][/yellow] - Update the [yellow]DB_NAME[/yellow] and [yellow]DB_COLLECTION_NAME[/yellow] for your [yellow]MongoDB[/yellow] database
        - [yellow][link={project_paths.MODELS}]models/__init__.py[/link][/yellow] - Update the [yellow]ExampleDB[/yellow] model

      [cyan]Frontend[/cyan]
        - [green][link={project_paths.LAYOUT}]app/layout.tsx[/link][/green] - Update the [green]metadata[/green] and [green]font style[/green]
        - [green][link={project_paths.HOMEPAGE}]pages/Homepage/Homepage.tsx[/link][/green] - Update the content for the [green]homepage[/green]\n
    """)
    )


if __name__ == "__main__":
    app()
