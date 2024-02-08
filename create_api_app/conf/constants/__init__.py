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

# Custom print emoji's
PASS = '[green]\u2713[/green]'
FAIL = '[red]\u274c[/red]'
PARTY = ':party_popper:'

# Set default static directory name
STATIC_DIR_NAME = 'public'

# Handle DB_TYPE selection
MONGO_URLS = 'DATABASE_URL=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/?retryWrites=true&w=majority'

SQL_URLS = 'DATABASE_URL=sqlite:///./database.db\n' + \
           '# DATABASE_URL=postgresql://<username>:<password>@postgresserver/db'

SQL_PACKAGES = [
    "sqlalchemy"
]

MONGO_PACKAGES = [
    "beanie",
    "motor"
]
