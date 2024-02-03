__Note: This project is a work in progress!__

# Create API App Quickstart Tool

Welcome to the quickstart tool for creating a `FastAPI` project with a `NextJS` frontend.

## Why This Tool?

Creating a project from scratch can be a tedious process. I've found limited tools for creating a `FastAPI` and `NextJS` app together that are suitable for my requirements. So, I built my own! 

I use this tool personally for `SaaS` and `ML API` projects and have found it extremely useful for immediately diving into coding without faffing around with minor setup details (except API keys!). Hopefully it's useful to you too!

The projects created using this tool come configured with a `development (dev)` and `production (prod)` mode that both use `Docker` containers to operate. More details on this below in the [Creation](#creation) section.

## The Stack

All projects are created using the same stack for simplicity, and to provide a template. Some options are configurable. Refer to the [Customisation and Configuration](#customisation-and-configuration) section for more details.

The main elements of the stack include:

- [FastAPI](https://github.com/tiangolo/fastapi)
- [NextJS](https://nextjs.org/)
- [TailwindCSS](https://tailwindcss.com/)

_Note: all libraries and packages are automatically installed to their latest versions when running the tool._

### Backend 

For the backend, the default packages installed include:

- `fastapi`
- `uvicorn[standard]`
- `python-dotenv`
- `poetry`

Additional packages installed (changeable):

- `langchain`

Development packages installed (changeable):

- `pytest`
- `pytest-cov`
- `hypothesis`

### Frontend

For the frontend, the default packages are:

- [NVM](https://docs.uploadthing.com/getting-started/appdir) - For managing the node package version
- [Clerk](https://clerk.com/) & [Clerk Themes](https://clerk.com/docs/components/customization/themes) - User management
- [Uploadthing](https://docs.uploadthing.com/) - File management
- [Shadcn UI](https://ui.shadcn.com/) - Component library

Additionally, the template uses styling elements from these two resources:

- [Shadcn UI Theme Generator](https://gradient.page/tools/shadcn-ui-theme-generator)
- [Modern Background Snippets](https://bg.ibelick.com/)

I encourage you to play around with them yourself!

## Dependencies

The tool is intended to be dynamic and aims to install the most recent packages where possible. To do this, we use [Node Version Manager (NVM)](https://github.com/nvm-sh/nvm?tab=readme-ov-file#intro) with `NPM` and [Python (currently 3.12.1)](https://www.python.org/downloads/). 

_Unfortunately, at the time of creating this [bun](https://bun.sh/) is experimental with Windows so we opted for `NPM` instead. [Issue request](https://github.com/Achronus/create-api-app/issues/2) added for future consideration._

The `Python` packages are stored within a `poetry` project in the `<project_name>/backend` directory. 

The `NextJS` application uses `node_modules` and is stored in the `<project_name>/frontend` directory.

This application is developed on a Windows machine so you may experience issues on `Linux/Mac OS`. I encourage you still to try it and flag any issues in the [issues](https://github.com/Achronus/create-api-app/issues) section. Compatibility has been considered but needs more rigorous testing ([Compatibility discussion here](https://github.com/Achronus/create-api-app/issues/3))!

## Customisation and Configuration

### Customisation

All files added to the project are stored in `setup_assets`. You can add additional files that you want but there are a few things to note:
1. `setup_assets` is divided into three parts: `backend`, `frontend`, `root` (no directory) 
2. `backend` files must be in the `setup_assets/backend` folder
3. `frontend` files must be in the `setup_assets/frontend` folder
4. Root project files must be in the root of `setup_assets` - e.g., `setup_assets/.gitignore`
5. Static files **MUST** be stored in a `setup_assets/frontend/static` folder
   - The static folder assets are moved automatically into the `<project_name>/frontend/public` folder

### Configuration

To customise the configuration go to `create_api_app/config.py`. Here you can:
- Change the database URL -> `DATABASE_URL`, which defaults to a SQLite local database.
- Add additional `backend` packages to the project -> `BACKEND_ADDITIONAL_PACKAGES`
- Add `backend` development packages to the project -> `BACKEND_DEV_PACKAGES`
- Add additional `.env` file variables -> `ENV_FILE_ADDITIONAL_PARAMS`

Most of the configuration options are treated as `list` items that accept `strings`, except the `DATABASE_URL` which is a `string` itself!

The database is automatically setup depending on the start of the `DATABASE_URL`. Currently the options are:
- SQLite
- PostgresSQL
- MongoDB


### Creation
1. To get started, clone the repository, enter the folder and run `create` with a `name` (e.g., `my_project`) argument inside a `poetry shell`. This creates a new project inside the `parent` directory of the `fastapi-quickstart` directory:

```bash
git clone https://github.com/Achronus/fastapi-quickstart.git
cd fastapi-quickstart
poetry shell
create my_project  # Replace me with custom name!
```

For example, if you have a parent folder called `projects` and are making a project called `todo_app` the project is created in `projects/todo_app` instead of `projects/fastapi-quickstart/todo_app`.


### And That's It!

Everything is setup with a blank template ready to start building a project from scratch. Run the following commands to run the docker `development` server and watch `TailwindCSS` locally!

Not got Docker? Follow these instructions from the [Docker website](https://docs.docker.com/get-docker/).


```bash
cd ../my_project  # Replace me with custom name!
docker-compose up -d --build

poetry shell
poetry install

watch
```

Then access the site at [localhost:8080](http://localhost:8080).


### Production

When configuring for production, remember to update the `ENV_TYPE` variable in `project_name/.env` from `dev` -> `prod`!

You can then use the same docker-compose command to run the production server in the environment of your choice.

```bash
docker-compose up -d --build
```


## Folder Structure

The newly created project should look similar to the following:

```bash
project_name
└── config
|   └── docker
|   |   └── Dockerfile.backend
└── project_name
|   └── backend
|   |   └── database
|   |   |   └── __init__.py
|   |   |   └── crud.py
|   |   |   └── models.py
|   |   |   └── schemas.py
|   |   └── routers
|   |   |   └── __init__.py
|   |   |   └── items.py
|   |   |   └── users.py
|   |   └── tests
|   |   |   └── __init__.py
|   |   └── utils
|   |   |   └── __init__.py
|   |   └── __init__.py
|   |   └── .env
|   |   └── dependencies.py
|   |   └── main.py
|   └── frontend
|   |   └── public
|   |   |   └── css
|   |   |   |   └── flowbite.min.css
|   |   |   |   └── input.css
|   |   |   |   └── style.min.css
|   |   |   └── imgs
|   |   |   |   └── avatar.svg
|   |   |   └── js
|   |   |       └── alpine.min.js
|   |   |       └── flowbite.min.js
|   |   |       └── htmx.min.js
|   |   |       └── theme-toggle.js
|   |   └── templates
|   |       └── components
|   |       |   └── navbar.html
|   |       └── _base.html
|   |       └── index.html
|   └── build.py
|   └── tailwind.config.js
|   └── tailwindcss OR tailwindcss.exe
└── .dockerignore
└── .env
└── .gitignore
└── database.db
└── docker-compose.yml
└── poetry.lock
└── pyproject.toml
└── README.md
```
