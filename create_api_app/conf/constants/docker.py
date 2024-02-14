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
        self.python_version_full = '3.12.1'
        self.python_version = ".".join(self.python_version_full.split(".")[:2])
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
        # DOCKER CONFIG SETTINGS
        # -------------------------
        PROJECT_NAME={self.config.project_name}

        # Uvicorn (FastAPI)
        POETRY_VERSION={self.config.poetry_version}
        HOST={self.config.host}
        BAK_PORT={self.config.bak_port}
        BAK_PORTS={self.config.bak_ports}
        PYTHON_BUILD_VERSION={self.config.python_version_full}
        PYTHON_SITE_PACKAGES_VERSION={self.config.python_version}

        # NextJS
        FNT_PORT={self.config.fnt_port}
        FNT_PORTS={self.config.fnt_ports}
        BUN_VERSION={self.config.bun_version}
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
        ARG BUILD_VERSION

        ########################################
        # --- Base ---
        ########################################
        FROM python:${{BUILD_VERSION}}-alpine as base

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
            PORT && \\
            ENV_MODE

        ENV PACKAGE_DIR=/usr/local/lib/python${{PYTHON_VERSION}}/site-packages \\
            PORT=${{PORT}} \\
            ENV_MODE=${{ENV_MODE}}

        # Copy files from builder
        COPY --from=builder /app /app/
        COPY --from=builder $PACKAGE_DIR $PACKAGE_DIR

        # Expose port
        EXPOSE $PORT

        # Run server
        # CMD ["sleep", "infinity"]
        CMD python -m build --env $ENV_MODE
        """)

    def frontend_df(self) -> str:
        """The content for the frontend Dockerfile."""
        return self.__format("""
        # Dockerfile for NextJS
        # https://hub.docker.com/r/oven/bun/tags
        ARG BUILD_VERSION

        ########################################
        # --- Base ---
        ########################################
        FROM oven/bun:${BUILD_VERSION}-alpine as base

        # Set working directory
        WORKDIR /app

        # Install yarn (to fix bun run bug)
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

        ########################################
        # --- Development Stage ---
        ########################################
        FROM base AS development

        ARG PORT
        ENV PORT=${PORT}

        # Copy files from builder
        COPY --from=builder /app/ /app/

        # Expose the required port
        EXPOSE $PORT

        # run server
        # CMD ["sleep", "infinity"]
        CMD ["bun", "run", "dev"]

        ########################################
        # --- Production Stage ---
        ########################################
        FROM builder AS prod_builder

        # build packages
        RUN bun run build

        ########################################
        FROM base AS production

        ARG PORT
        ENV PORT=${PORT}

        # Copy the build output
        COPY --from=prod_builder /app/public /app/public
        COPY --from=prod_builder --chown=nextjs:nodejs /app/.next/standalone /app/
        COPY --from=prod_builder --chown=nextjs:nodejs /app/.next/static /app/.next/static

        # Expose the required port
        EXPOSE $PORT

        # server.js is created by next build from the standalone output
        # https://nextjs.org/docs/pages/api-reference/next-config-js/output
        CMD ["node", "server.js"]
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
            container_name: backend_dev
            build:
              context: .
              dockerfile: Dockerfile.backend
              args:
                POETRY_VERSION: ${POETRY_VERSION}
                PORT: ${BAK_PORT}
                PYTHON_VERSION: ${PYTHON_SITE_PACKAGES_VERSION}
                BUILD_VERSION: ${PYTHON_BUILD_VERSION}
                ENV_MODE: dev
            ports:
            - "${BAK_PORTS}"
            volumes:
            - .:/${PROJECT_NAME}
                             
          frontend:
            container_name: frontend_dev
            build:
              context: .
              dockerfile: Dockerfile.frontend
              target: development
              args:
                PORT: ${FNT_PORT}
                BUILD_VERSION: ${BUN_VERSION}
            ports:
            - "${FNT_PORTS}"
            volumes:
            - .:/${PROJECT_NAME}
        """)

    def compose_prod(self) -> str:
        """The content for the production Docker Compose file."""
        return self.__format("""
        # Run command:
        # docker-compose -f docker-compose.prod.yml up -d --build 

        # Exit command:
        # docker-compose down

        version: '1'

        services:
          backend:
            extends:
              file: docker-compose.yml
              service: backend
            container_name: backend_prod
            build:
              args:
                ENV_MODE: prod
                             
          frontend:
            extends:
              file: docker-compose.yml
              service: frontend
            container_name: frontend_prod
            build:
              target: production
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
            (self.paths.COMPOSE_PROD, self.content.compose_prod()),
            (self.paths.IGNORE, self.content.dockerignore())
        ]
