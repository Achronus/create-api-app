

# Change venv activation depending on OS
VENV_NAME = 'env'

# Define core backend packages
CORE_BACKEND_PACKAGES = [
    "fastapi", 
    "uvicorn[standard]", 
    "python-dotenv"
]

# Development backend packages to install
BACKEND_DEV_PACKAGES = [
    "pytest",
    "pytest-cov",
    "hypothesis"
]

# Define core NPM packages to install
NPM_PACKAGES = [
    "tailwind-merge",
    "tailwindcss-animate", 
    "flowbite", 
    "next-themes",  # Shadcn/ui
    "uploadthing",
    "@uploadthing/react",
    "@clerk/nextjs",
    "@clerk/themes",
    "zod"
]

# Custom print emoji's
PASS = '[green]\u2713[/green]'
FAIL = '[red]\u274c[/red]'
PARTY = ':party_popper:'

# Set default static directory name
STATIC_DIR_NAME = 'public'
