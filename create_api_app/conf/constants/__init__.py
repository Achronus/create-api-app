# Define core backend packages
BACKEND_CORE_PACKAGES = [
    "fastapi",
    "uvicorn[standard]",
    "python-dotenv",
    "beanie",
]

# Development backend packages to install
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

# Set default static directory name
STATIC_DIR_NAME = "public"
