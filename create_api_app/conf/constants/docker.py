import textwrap

from .filepaths import get_project_name, get_poetry_version, DockerPaths


class DockerEnvConfig:
    def __init__(self) -> None:
        self.poetry_version = get_poetry_version()
        self.project_name = get_project_name()

        # Docker-compose
        self.ports = "8080:80"

        # Uvicorn
        self.port = self.ports.split(':')[-1]
        self.host = "0.0.0.0"

        self.python_version = '3.12'
        self.version_extension = '.1'


class DockerContent:
    def __init__(self) -> None:
        self.dotenv_config = DockerEnvConfig()

    @staticmethod
    def __format(content: str) -> str:
        """Helper function for formatting file content."""
        return textwrap.dedent(content)[1:]

    def env_config(self) -> str:
        return self.__format(f"""
        #--------------------------
        # ENVIRONMENT SETTINGS
        #--------------------------
        # !IMPORTANT! CHANGE TO 'prod' WHEN IN PRODUCTION
        # Options: 'dev' or 'prod'
        ENV_TYPE=dev
        
        #--------------------------
        # DOCKER CONFIG SETTINGS
        # -------------------------
        # Docker config
        POETRY_VERSION={self.dotenv_config.poetry_version}
        PROJECT_NAME={self.dotenv_config.project_name}
        PORTS={self.dotenv_config.ports}

        # Uvicorn
        PORT={self.dotenv_config.port}
        HOST={self.dotenv_config.host}
        """)
    
    def dockerignore(self) -> str:
        return self.__format("""
        # Git
        **.git
        *.gitignore

        # Python
        **/__pycache__

        # Docker
        /config**/docker
        *docker-compose.yml
        *.dockerignore

        # Tailwind
        **tailwindcss
        **tailwindcss.exe
        **tailwind.config.js

        # Project
        **/data

        # Dev
        **/tests
        *pytest.ini
        **/.pytest_cache
        """)

    def backend_df(self) -> str:
        """The content for the backend Dockerfile."""
        start = f"""
        # Dockerfile for FastAPI
        ARG PYTHON_VERSION={self.dotenv_config.python_version}
        ARG BUILD_VERSION=${{PYTHON_VERSION}}{self.dotenv_config.version_extension}
        """

        return self.__format(start + """
        ########################################
        # --- Base ---
        ########################################
        FROM python:${BUILD_VERSION}-alpine as base

        ARG PROJECT_NAME
        ENV PROJECT_NAME=${PROJECT_NAME}

        # Set working directory
        WORKDIR /$PROJECT_NAME

        ########################################
        # --- Builder Stage ---
        ########################################
        FROM base as builder

        ARG POETRY_VERSION

        # Set environment variables
        ENV PYTHONFAULTHANDLER=1 \\
            PYTHONUNBUFFERED=1 \\
            PYTHONHASHSEED=random \\
            # PIP config
            PIP_NO_CACHE_DIR=off \\
            PIP_DISABLE_PIP_VERSION_CHECK=on \\
            PIP_DEFAULT_TIMEOUT=100 \\
            # Poetry config
            POETRY_VERSION=${POETRY_VERSION}

        # Copy project and poetry files
        COPY . .

        # install system dependencies, update pip, install poetry, its packages, and cleanup
        RUN apk update && \\
            apk add --no-cache --virtual .build-deps build-base && \\
            pip install --upgrade pip "poetry==$POETRY_VERSION" && \\
            poetry config virtualenvs.create false && \\
            poetry install --only main && \\
            apk del .build-deps

        ########################################
        # --- Runtime Stage ---
        ########################################
        FROM base as runtime

        ARG PYTHON_VERSION && \\
            PORT

        ENV PROJECT_NAME=${PROJECT_NAME} \\
            PACKAGE_DIR=/usr/local/lib/python${PYTHON_VERSION}/site-packages \\
            PORT=${PORT}

        # Copy files from builder
        COPY --from=builder $PROJECT_NAME .
        COPY --from=builder $PACKAGE_DIR $PACKAGE_DIR

        # Expose port
        EXPOSE $PORT
        """)

    def compose_main(self) -> str:
        """The content for the main (entry point) Docker Compose file."""
        return self.__format("""
        # Run command:
        # docker-compose --env-file .env.prod up -d --build

        # Exit command:
        # docker-compose --env-file .env.prod down

        version: '1'

        services:
        backend:
            container_name: backend
            build:
              context: .
              dockerfile: ./config/docker/Dockerfile.backend
              args:
                POETRY_VERSION: ${POETRY_VERSION}
                PROJECT_NAME: ${PROJECT_NAME}
                PORT: ${PORT}
            ports:
            - "${PORTS}"
            volumes:
            - .:/${PROJECT_NAME}
            # entrypoint: ['sleep', 'infinity']
            entrypoint: ["python", "-m", "${PROJECT_NAME}.build"]
        """)


class DockerFileMapper:
    def __init__(self) -> None:
        self.content = DockerContent()
        self.paths = DockerPaths()

    def dockerfiles(self) -> list[tuple[str, str]]:
        """Maps the pairs of filepaths and content for Dockerfiles."""
        return [
            (self.paths.BACKEND_DF, self.content.backend_df())
        ]

    def compose_files(self) -> list[tuple[str, str]]:
        """Maps the pairs of filepaths and content for Docker compose files."""
        return [
            (self.paths.COMPOSE_MAIN, self.content.compose_main()),
            (self.paths.IGNORE, self.content.dockerignore())
        ]
