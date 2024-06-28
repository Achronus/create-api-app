# Create API App Quickstart Tool <!-- omit in toc -->

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/create-api-app?style=flat&color=green)

Welcome to the quickstart tool for creating a `FastAPI` project with a `NextJS` frontend.

This tool creates a predefined template while installing the most recent packages where possible.

Found on:

- [PyPi](https://pypi.org/project/create-api-app/)
- [GitHub](https://github.com/Achronus/create-api-app/)

## Contents <!-- omit in toc -->

- [Why This Tool?](#why-this-tool)
- [The Stack](#the-stack)
- [Installation](#installation)
- [Running The Backend](#running-the-backend)
- [Running the Frontend](#running-the-frontend)
- [Customization](#customization)

## Why This Tool?

Creating a project from scratch can be a tedious process. Not only do you have to create all the files yourself, it typically requires a lot of small minor changes that can easily be automated. So, rather than wasting a lot of time setting up projects, I created a tool that does it all for me!

I use this tool personally for `SaaS` and `ML API` projects and have found it extremely useful for immediately diving into coding without faffing around with setup details (except for configuring API keys). Hopefully, it's useful to you too!

## The Stack

All projects are created using the same stack, consisting of the following:

1. Backend

   - [FastAPI](https://github.com/tiangolo/fastapi)
   - [Pydantic](https://docs.pydantic.dev/)
   - [MongoDB](https://www.mongodb.com/)
   - [Beanie](https://beanie-odm.dev/)
   - [Poetry](https://python-poetry.org/)
   - [Pytest](https://docs.pytest.org/)
   - [Hypothesis](https://hypothesis.readthedocs.io/)

2. Frontend

   a. Core:

     - [NextJS](https://nextjs.org/)
     - [TailwindCSS](https://tailwindcss.com/)
     - [TypeScript](https://www.typescriptlang.org/)
     - [Lucide React](https://lucide.dev/)
     - [Shadcn UI](https://ui.shadcn.com/)

   b. Optional:
     - [Clerk](https://clerk.com/docs/quickstarts/nextjs)
     - [Uploadthing](https://uploadthing.com/)
     - [Stripe](https://stripe.com/docs)

_Note: all libraries and packages are automatically installed to their latest versions when running the tool._

We've also added some extra files too! You can find out more about them in our [documentation](https://create.achronus.dev/file-structure/).

## Installation

1. Firstly, install [Docker](https://docs.docker.com/get-docker/), we use this to create the frontend files dynamically using the [Build NextJS App Tool](https://github.com/Achronus/build-nextjs-app).

2. Install the package through `PIP`:

   ```python
   pip install create_api_app
   ```

3. Create a project with a `name` and an `optional` string of `exclusion` characters for the `optional` packages.

   Exclusion options: `c`, `u`, `s`, `cs`, `cu`, `us`, `cus`.
   _`c` = `Clerk`, `u` = `Uploadthing`, `s` = `Stripe`_

   ```python
   create-api-app <project_name> <exclusions>
   ```

And that's it! You'll find two folders in your project, one called `frontend` (for NextJS) and another called `backend` (for FastAPI).

## Running The Backend

1. Open a terminal and navigate to the `backend` directory:

   ```cmd
   cd backend
   ```

2. Install a virtual environment for `Poetry`:

   ```cmd
   python -m venv env
   ```

3. Access it using one of the following (first -> `Windows`; second -> `Mac/Linux`):

   ```cmd
   .\env\Scripts\activate
   ```

   ```cmd
   source ./env/bin/activate
   ```

   _Not working? Refer to the [virtual env docs](https://docs.python.org/3/library/venv.html#how-venvs-work)._

4. Run the `uvicorn` server using the `Poetry` script:

   ```cmd
   app-start
   ```

## Running the Frontend

1. Open a terminal and navigate to the `frontend` directory:

   ```cmd
   cd frontend
   ```

2. Install the packages using [Node.js](https://nodejs.org/en):

   ```cmd
   npm install
   ```

3. Run the development server:

   ```cmd
   npm run dev
   ```

## Customization

Customization options are found in our [documentation](https://create.achronus.dev/customization/).
