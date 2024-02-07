__Note: This project is a work in progress and does NOT currently work! Check back once a version is released!__

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

As mentioned previously, we've limited the customisation to the `DATABASE_TYPE`. Originally, we planned to provide additional commands for adding packages but realised it defeats the purpose of the tool. 

The tool is designed to provide a base template for `FastAPI` and `NextJS` projects, allowing developers to quickly create a skeleton project that they can configure themselves. Adding extra unnecessary complexity would only makes things more complicated, so we went back to basics and focused on the essentials.

Fortunately, this reduced the tool down to two simple commands: `docker build` and `docker run`. We'll discuss this more in the next section.

Firstly, we want to highlight that the appropriate dependencies are automatically setup depending on the `DATABASE_TYPE`. This has two valid options:

- SQL
- Mongo

Depending on the selection, the backend of the database will automatically be setup with either [sqlalchemy](https://www.sqlalchemy.org/) or [beanie](https://beanie-odm.dev/), respectively.

For simplicity, when selecting `SQL` (the default option) we've configured the backend with a `SQLite` database and make it easy to switch to other ones. 

SQL is typically easier to implement, due to the [FastAPI documentation](https://fastapi.tiangolo.com/tutorial/sql-databases/?h=sql). However, we personally prefer `MongoDB` due to its [sustainability goals](https://www.mongodb.com/company/sustainability), so we cannot help but encourage others to use it as well!


## Using The Tool
_❔ Not got Docker? Follow these instructions from the [Docker website](https://docs.docker.com/get-docker/)_.

1. To get started, clone the repository, enter the folder and run the docker commands:

```bash
git clone https://github.com/Achronus/create-api-app.git
cd create-api-app
docker build ?
docker run ?
```

In your terminal, you should get feedback from the container stating the progress of the projects creation. Once complete you a new folder is added inside it with the desired `<project_name>`. Move the folder to where you want, and then tweak it as need. 

_❗ Note: We use the `-rm` flag in the `Docker` commands to automatically clean up the container and its images, removing them after the project is successfully built._

## Starting A Created Project

You'll need to update the `backend/.env.local` and `frontend/.env.local` files before you can work with the project. 

The `backend/.env.local` is the easiest. Just select and update the `DATABASE_URL` you want to use.

`frontend/.env.local` is a little more time consuming, but pretty self-explanatory. Open the URLs provided in the file, create an account (or use an existing one), and fill in the API key details for each one. Feel free to remove any variables you don't need or want! 

With everything setup, enter the `<project_name>` directory and start the `dev` server using the following command run:

```bash
cd <file_path>/<project_name>  # Navigate to the project directory...
docker-compose -d --build
```

Then access the backend at [localhost:8080](http://localhost:8080) and frontend at [localhost:3000](http://localhost:3000).

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

When moving to production, update the `ENV_TYPE` variable in `<project_name>/.env` from `dev` -> `prod`!

Then use the docker-compose command with the production file to run the production environment.

```bash
docker-compose -f docker-compose.prod.yml -d --build
```

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
|   |   └── dependencies.py
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
└── Dockerfile.frontend.prod
```
