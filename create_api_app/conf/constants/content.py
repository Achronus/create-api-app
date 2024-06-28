from create_api_app.conf.storage import Packages


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

    @classmethod
    def ut_remote_pattern(cls) -> list[str]:
        """Provides the `uploadthing` `remotePattern` found in the `next.config.mjs` file."""
        return [
            "      {\n",
            '        protocol: "https",\n',
            '        hostname: "utfs.io",\n',
            "        pathname: `/a/${process.env.NEXT_PUBLIC_UPLOADTHING_APP_ID}/*`,\n",
            "      },\n",
        ]


class EnvFileContent:
    """A helper class for creating the `.env.local` file."""

    def __init__(self, packages: Packages) -> None:
        self.packages = packages

    def uploadthing(self) -> list[str]:
        """Returns the `Uploadthing` API key content."""
        return [
            "# Uploadthing: storing files and handling file uploading",
            "# https://uploadthing.com/",
            "UPLOADTHING_SECRET=",
            "NEXT_PUBLIC_UPLOADTHING_APP_ID=",
            "",
        ]

    def clerk(self) -> list[str]:
        """Returns the `Clerk` API key content."""
        return [
            "# Clerk: User Authentication",
            "# https://clerk.com/docs/quickstarts/nextjs",
            "NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=",
            "CLERK_SECRET_KEY=",
            "",
            "NEXT_PUBLIC_CLERK_SIGN_IN_URL=/auth/sign-in",
            "NEXT_PUBLIC_CLERK_SIGN_UP_URL=/auth/sign-up",
            "NEXT_PUBLIC_CLERK_AFTER_SIGN_IN_URL=/",
            "NEXT_PUBLIC_CLERK_AFTER_SIGN_UP_URL=/",
            "",
        ]

    def stripe(self) -> list[str]:
        """Returns the `Sstripe` API key content."""
        return [
            "# Stripe: user payments",
            "# https://stripe.com/docs",
            "NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=",
            "STRIPE_SECRET_KEY=",
            "STRIPE_WEBHOOK_SECRET=",
            "NEXT_PUBLIC_STRIPE_CLIENT_ID=",
            "NEXT_PUBLIC_PLATFORM_SUBSCRIPTION_PERCENT=1",
            "NEXT_PUBLIC_PLATFORM_ONETIME_FEE=2",
            "NEXT_PUBLIC_PLATFORM_PERCENT=1",
            "NEXT_PRODUCT_ID=",
            "",
        ]

    def make(self) -> str:
        """Creates the `env` file content."""
        map = {
            "clerk": self.clerk(),
            "uploadthing": self.uploadthing(),
            "stripe": self.stripe(),
        }

        content = []
        for package in self.packages.items:
            if not package.exclude:
                content.extend(map[package.name])

        return "\n".join(content)
