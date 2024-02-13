# Create API App Quickstart Tool

Welcome to the quickstart tool for creating a `FastAPI` project with a `NextJS` frontend.

## Why This Tool?

Creating a project from scratch can be a tedious process. Not only do you have to create all the files yourself, it typically requires a lot of small minor changes that can easily be automated. So, rather than wasting a lot of time setting up projects, I created a tool that does it all for me! 

I use this tool personally for `SaaS` and `ML API` projects and have found it extremely useful for immediately diving into coding without faffing around with setup details (except for configuring API keys). Hopefully, it's useful to you too!

## The Stack

All projects are created using the same stack. To maintain a consistent template, and keep things simple, we've limited the customisation to one parameter: a `DATABASE_URL`. Refer to the [Customisation and Configuration](#customisation-and-configuration) section for more details.

The project stack contains three main elements:

- [FastAPI](https://github.com/tiangolo/fastapi)
- [NextJS](https://nextjs.org/)
- [TailwindCSS](https://tailwindcss.com/) & [Flowbite](https://flowbite.com/)

_Note: all libraries and packages are automatically installed to their latest versions when running the tool._

### Backend 

For the backend, we use [poetry](https://python-poetry.org/) to manage our dependencies and install the following default packages:

#### Production 
- `fastapi`
- `uvicorn[standard]`
- `python-dotenv`
- `poetry`

#### Development

- `pytest`
- `pytest-cov`
- `hypothesis`

### Frontend

For the frontend, we use [bun](https://bun.sh/) with [Node Version Manager (NVM)](https://github.com/nvm-sh/nvm?tab=readme-ov-file#intro) to manage our packages. By default we install:

- [Clerk](https://clerk.com/) & [Clerk Themes](https://clerk.com/docs/components/customization/themes) - User management
- [Uploadthing](https://docs.uploadthing.com/) - File management
- [Shadcn UI](https://ui.shadcn.com/) - Component library

Additionally, the template uses styling elements from these two resources:

- [Shadcn UI Theme Generator](https://gradient.page/tools/shadcn-ui-theme-generator)
- [Modern Background Snippets](https://bg.ibelick.com/)

I encourage you to play around with them yourself!

## Dependencies

The tool is intended to be dynamic and aims to install the most recent packages where possible, while maintaining compatibility across the main OS's (Mac, Linux and Windows). After reviewing multiple tools, we decided [Docker](https://www.docker.com/) was the best solution for our purpose. Also, the projects the tool creates use `Docker` themselves, so it really was a no brainer!

We use `docker-compose` to switch between `development (dev)` and `production (prod)` seamlessly, and make the project management easy by separating the `frontend` and `backend` into separate containers.

We store the `Python` `poetry` project in the `<project_name>/backend` directory (for the FastAPI app), and the `NextJS` application (that uses `node_modules`) in the `<project_name>/frontend` directory.

We've taken great care to try to maximise compatibility across the main OS's, but still expect bugs to surface. If there are any issues using the tool, please flag them in the [issues](https://github.com/Achronus/create-api-app/issues) section of this repository.

## Customisation and Configuration

We've limited the tool customisation to the `DB_TYPE`, `PROJECT_NAME`, and the `<project_name>/.env` file. Originally, we planned to provide additional commands for adding packages but realised it defeats the purpose of the tool. 

The tool is designed to provide a base template for `FastAPI` and `NextJS` projects, allowing developers to quickly create a skeleton project that they can configure themselves. Adding extra unnecessary complexity would only makes things more complicated, so we went back to basics and focused on the essentials.

### Database

It's worth noting, the appropriate dependencies are automatically setup depending on the `DB_TYPE` and configured with appropriate file templates. This has two valid options: `['sql', 'mongo']`.

If `sql` we install:

- [sqlalchemy](https://www.sqlalchemy.org/)

If `mongo` we install:

- [beanie](https://beanie-odm.dev/)
- [motor](https://motor.readthedocs.io/en/stable/)

For simplicity, we've configured the default to `SQL` with a `SQLite` database. SQL is typically easier to implement, due to the [FastAPI documentation](https://fastapi.tiangolo.com/tutorial/sql-databases/?h=sql). However, we personally prefer `MongoDB` due to its [sustainability goals](https://www.mongodb.com/company/sustainability), so we cannot help but encourage others to use it as well!

The `<project_name>/.env` file focuses on the docker file configuration. For example, here you can configure the `PYTHON_VERSION` to use and the `BUN_VERSION`, along with the `PORTS` and `HOST`. 

When modifiying the `PYTHON_VERSION`, be aware there are two variables: one for the `BUILD` and another for the `SITE_PACKAGES`. Annoyingly, there is no way to 'trim' the build version in a Dockerfile for the site packages, so we've had to use two separate variables instead. Keep in mind `SITE_PACKAGES` can only be `X.Y` while `BUILD` can be `X.Y` or `X.Y.Z`.

## Using The Tool
_❔ Not got Docker? Follow these instructions from the [Docker website](https://docs.docker.com/get-docker/)_.

### Local Install

1. To get started, clone the repository, enter the folder and run the docker commands (replacing `<project_name>` and `<path>` with a custom one!):

```bash
git clone https://github.com/Achronus/create-api-app.git
cd create-api-app

# Build the image
docker build -t create_api_app .

# Run the tool using a container
docker run -it -e PROJECT_NAME=<project_name> -e DB_TYPE=sql --name creating_project create_api_app

# Copy files from container to local device
docker cp creating_project:/app/<project_name> <path>/<project_name>
```

2. Cleanup files (optional):

```bash
# Remove container only
docker container rm creating_project -f

# Remove container and image
docker container rm creating_project -f && docker image rm create_api_app -f
```

### Docker Hub (Recommended)

Alternatively, you can download the docker image from the hub (remember to replace `<project_name>` and `<path>` with a custom one!):

```bash
# Get the image
docker pull achronus/create_api_app:latest

# Run the tool using a container
docker run -it -e PROJECT_NAME=<project_name> -e DB_TYPE=sql --name creating_project create_api_app

# Copy files from container to local device
docker cp creating_project:/app/<project_name> <path>/<project_name>
```

In your terminal, you should get feedback from the container stating the progress of the projects creation. Once complete, use the `cp` command to copy the project to your desired location and then tweak it as need. 

_❗ Note: We use the `-it` flag to display colour formatting for the console, use `creating_project` as the container name and `create_api_app` as the image name._

## Starting A Created Project

You'll need to update the `backend/.env.local` and `frontend/.env.local` files before you can work with the project. 

1. The `backend/.env.local` is the easiest. Just update the `DATABASE_URL` with your `username`, `password`, and `cluster` (if needed, denoted with `<>`).
2. `frontend/.env.local` is a little more time consuming, but pretty self-explanatory. Open the URLs provided in the file, create an account (or use an existing one), and fill in the API key details for each one. Feel free to remove any variables you don't need or want! 

3. With everything setup, enter the `<project_name>` directory and start the `dev` server using the following command:

```bash
cd <file_path>/<project_name>  # Navigate to the project directory...
docker-compose up -d --build
```

Then access the backend at [localhost:8080](http://localhost:8080) and frontend at [localhost:3000](http://localhost:3000).

_💡 Pro-tip: We've configured the docker container names to include `_dev` or `_prod` so you can quickly check which environment you are running!_

### Running Unit Tests In Development

Testing from a docker container is a little complicated, so instead we advise performing standard testing procedures from your local machine. 

With the `backend`, we can use a `poetry shell` to run our unit tests with `pytest`. Simply, access a shell, install the packages and run `pytest` like normal.

```bash
cd backend
poetry shell
poetry install
pytest
```

### Moving To Production

We've made it extremely easy to move from development to production. Simply test that everything works by running the production docker-compose file:

```bash
docker-compose -f docker-compose.prod.yml up -d --build
```

`NextJS` is automatically built and streamlined into a minified format, and `FastAPI` removes the `--reload` flag. If all works, you're good to go!

### Folder Structure

The newly created project should look similar to the following:

```bash
<project_name>
└── backend  # FastAPI
|   └── app
|   |   └── config
|   |   |   └── ...
|   |   └── db
|   |   |   └── ...
|   |   └── routers
|   |   |   └── ...
|   |   └── utils
|   |   |   └── ...
|   |   └── __init__.py
|   |   └── dependencies.py  # SQL only
|   |   └── main.py
|   └── tests
|   |   └── ...
|   └── __init__.py
|   └── .env.local
|   └── .gitignore
|   └── build.py
|   └── poetry.lock
|   └── pyproject.toml
|   └── pytest.ini
|   └── README.md
└── frontend  # NextJS
|   └── public
|   |   └── ...
|   └── src
|   |   └── app
|   |   |   └── ...
|   |   └── middleware.ts
|   └── .env.local
|   └── .eslintrc.json
|   └── .gitignore
|   └── bun.lockb
|   └── next.config.mjs
|   └── next-env.d.ts
|   └── package.json
|   └── postcss.config.js
|   └── README.md
|   └── tailwind.config.ts
|   └── tsconfig.json
└── .dockerignore
└── .env
└── docker-compose.prod.yml
└── docker-compose.yml
└── Dockerfile.backend
└── Dockerfile.frontend
```
