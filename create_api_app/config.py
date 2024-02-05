# Define your database URL
DATABASE_URL = 'sqlite:///./database.db'
# DATABASE_URL = "postgresql://<username>:<password>@postgresserver/db"

# Additional backend packages to install
BACKEND_ADDITIONAL_PACKAGES = [
    "langchain",
]

# Development backend packages to install
BACKEND_DEV_PACKAGES = [
    "pytest",
    "pytest-cov",
    "hypothesis"
]

# .env file additional parameters
ENV_FILE_ADDITIONAL_PARAMS = [
    # f'example={example}'  # example
]
