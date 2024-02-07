import textwrap

from .filepaths import (
    AssetFilenames, 
    get_project_name, 
    get_poetry_version, 
    DockerPaths
)


class DockerEnvConfig:
    def __init__(self) -> None:
        self.poetry_version = get_poetry_version()
        self.project_name = get_project_name()

        # Docker-compose
        self.env_name = AssetFilenames.PROD_ENV
        self.host = "0.0.0.0"

        self.bak_ports = "8080:80"
        self.bak_port = self.bak_ports.split(':')[-1]

        self.fnt_ports = "3000:3000"
        self.fnt_port = self.fnt_ports.split(':')[-1]

        # Dockerfiles
        self.python_version = '3.12'
        self.version_extension = '.1'

        self.bun_version = '1.0.26'


class DockerContent:
    def __init__(self) -> None:
        self.config = DockerEnvConfig()

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
        PROJECT_NAME={self.config.project_name}
        HOST={self.config.host}

        # Uvicorn (FastAPI)
        POETRY_VERSION={self.config.poetry_version}
        BAK_PORT={self.config.bak_port}
        BAK_PORTS={self.config.bak_ports}
        
        # NextJS
        FNT_PORT={self.config.fnt_port}
        FNT_PORTS={self.config.fnt_ports}
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
        return self.__format(f"""
        # Dockerfile for FastAPI
        # https://hub.docker.com/_/python/tags
        ARG PYTHON_VERSION={self.config.python_version}
        ARG BUILD_VERSION=${{PYTHON_VERSION}}{self.config.version_extension}

        ########################################
        # --- Base ---
        ########################################
        FROM python:${{BUILD_VERSION}}-alpine as base

        ARG PROJECT_NAME
        ENV PROJECT_NAME=${{PROJECT_NAME}}

        # Set working directory
        WORKDIR /app

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
            POETRY_VERSION=${{POETRY_VERSION}}

        # Copy project and poetry files
        COPY /backend {self.config.env_name} /app/

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

        ENV PROJECT_NAME=${{PROJECT_NAME}} \\
            PACKAGE_DIR=/usr/local/lib/python${{PYTHON_VERSION}}/site-packages \\
            PORT=${{PORT}}

        # Copy files from builder
        COPY --from=builder /app /app/
        COPY --from=builder $PACKAGE_DIR $PACKAGE_DIR

        # Expose port
        EXPOSE $PORT
        """)

    def frontend_df(self) -> str:
        """The content for the frontend Dockerfile."""
        return self.__format(f"""
        # Dockerfile for NextJS
        # https://hub.docker.com/r/oven/bun/tags
        ARG BUILD_VERSION=${self.config.bun_version}

        ########################################
        # --- Base ---
        ########################################
        FROM oven/bun:${{BUILD_VERSION}}-alpine as base

        ARG PROJECT_NAME
        ENV PROJECT_NAME=${{PROJECT_NAME}}

        # Set working directory
        WORKDIR /app
                             
        # Install yarn (mitigates bun NextJS run bug)
        RUN apk update && \\
            apk add --no-cache curl bash yarn

        ########################################
        # --- Builder Stage ---
        ########################################
        FROM base AS builder

        # Copy project files
        COPY /frontend /app

        # Install packages
        RUN bun install

        # ########################################
        # # --- Runtime Stage ---
        # ########################################
        FROM base AS runtime

        ARG PORT
        ENV PORT=${{PORT}}

        # Copy files from builder
        COPY --from=builder /app/ /app/

        # Expose the required port
        EXPOSE $PORT

        # run server
        # CMD ["sleep", "infinity"]
        CMD ["yarn", "run", "dev"]
        """)

    def compose_main(self) -> str:
        """The content for the main (entry point) Docker Compose file."""
        return self.__format("""
        # Run command:
        # docker-compose up -d --build

        # Exit command:
        # docker-compose down

        version: '1'

        services:
          backend:
            container_name: backend
            build:
              context: .
              dockerfile: Dockerfile.backend
              args:
                POETRY_VERSION: ${POETRY_VERSION}
                PROJECT_NAME: ${PROJECT_NAME}
                PORT: ${BAK_PORT}
            ports:
            - "${BAK_PORTS}"
            volumes:
            - .:/${PROJECT_NAME}
            # entrypoint: ['sleep', 'infinity']
            entrypoint: ["python", "-m", "build"]
                             
          frontend:
            container_name: frontend
            build:
              context: .
              dockerfile: Dockerfile.frontend
              args:
                PROJECT_NAME: ${PROJECT_NAME}
                PORT: ${FNT_PORT}
            volumes:
            - .:/${PROJECT_NAME}
            ports:
            - "${FNT_PORTS}"
        """)


class DockerFileMapper:
    def __init__(self) -> None:
        self.content = DockerContent()
        self.paths = DockerPaths()

    def dockerfiles(self) -> list[tuple[str, str]]:
        """Maps the pairs of filepaths and content for Dockerfiles."""
        return [
            (self.paths.BACKEND_DF, self.content.backend_df()),
            (self.paths.FRONTEND_DF, self.content.frontend_df())
        ]

    def compose_files(self) -> list[tuple[str, str]]:
        """Maps the pairs of filepaths and content for Docker compose files."""
        return [
            (self.paths.COMPOSE_MAIN, self.content.compose_main()),
            (self.paths.IGNORE, self.content.dockerignore())
        ]
