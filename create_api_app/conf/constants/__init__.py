from enum import StrEnum

from create_api_app.conf.storage import Package, Packages


# Define core backend packages
BACKEND_CORE_PACKAGES = [
    "fastapi",
    "uvicorn[standard]",
    "python-dotenv",
    "beanie",
]

# Define dev backend packages
BACKEND_DEV_PACKAGES = [
    "pytest",
    "pytest-cov",
    "hypothesis",
    "aiohttp",
    "requests",
]

# Custom print emoji's
PASS = "[green]\u2713[/green]"
FAIL = "[red]\u274c[/red]"
PARTY = ":party_popper:"


class ExcludeOptions(StrEnum):
    clerk = "c"
    uploadthing = "u"
    stripe = "s"
    clerk_n_stripe = "cs"
    clerk_n_uploadthing = "cu"
    uploadthing_n_stripe = "us"
    all = "cus"


clerk = Package(
    name="clerk",
    letter="c",
    dependencies=["@clerk/nextjs"],
    colour="cyan",
)
uploadthing = Package(
    name="uploadthing",
    letter="u",
    dependencies=["uploadthing", "@uploadthing/react"],
    colour="red",
)
stripe = Package(
    name="stripe",
    letter="s",
    dependencies=["@stripe/react-stripe-js", "@stripe/stripe-js"],
    colour="magenta",
)

PACKAGES = Packages([clerk, uploadthing, stripe])
