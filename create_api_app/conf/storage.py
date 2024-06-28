from dataclasses import dataclass


@dataclass
class Package:
    """Represents a single package."""

    name: str
    letter: str
    dependencies: list[str]
    colour: str
    exclude: bool = False

    def update_exclude(self, exclude: str) -> None:
        """Updates `self.exclude` to `True` if its `self.letter` exists in the `exclude` parameter."""
        self.exclude = True if self.letter in exclude else False

    def name_str(self) -> str:
        """Returns the name wrapped in its colour as a string."""
        return f"[{self.colour}]{self.name}[/{self.colour}]"


@dataclass
class Packages:
    """Stores multiple packages."""

    items: list[Package]

    def update(self, exclude: str) -> None:
        """Updates the packages based on the given parameters."""
        if exclude:
            for package in self.items:
                package.update_exclude(exclude)

    def exclusions(self) -> list[Package]:
        """Retrieves the packages that are excluded from the project."""
        return [package for package in self.items if package.exclude]


@dataclass
class RemotePattern:
    """A storage container representing a `remotePattern` found in the `next.config.mjs`."""

    protocol: str = None
    hostname: str = None
    pathname: str = None
