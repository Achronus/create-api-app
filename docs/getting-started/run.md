# Running The Project

In development, you need to use two separate terminal windows to run the `backend` and `frontend` independently.

You can read more about the specific steps for each below.

## Backend

??? info "Virtual Environment Not Working?"
    Refer to the [Python documentation](https://docs.python.org/3/library/venv.html#how-venvs-work).

1. Open a terminal and navigate to the `backend` directory:

    ```cmd title=""
    cd backend
    ```

2. Install a virtual environment for `Poetry`:

    ```cmd title=""
    python -m venv env
    ```

3. Access it using one of the following:

    ```cmd title="For Windows"
    .\env\Scripts\activate
    ```

    ```cmd title="For Mac/Linux"
    source ./env/bin/activate
    ```

4. Run the `uvicorn` server using the `Poetry` script:

    ```cmd title=""
    app-start
    ```

## Frontend

??? note "Dependency Management Options"
    While we show `npm` in the example snippets here, you don't have to use it if you don't want to. We know that `npm` is often very slow compared to other dependency managers but have found its the easiest to use on `Windows`.
    
    Here are a few alternatives to explore if you want something faster:

    - [pnpm](https://pnpm.io/)
    - [yarn](https://classic.yarnpkg.com/en/)
    - [bun](https://bun.sh/)

1. Open a terminal and navigate to the `frontend` directory:

    ```cmd title=""
    cd frontend
    ```

2. Install the packages using [`Node.js`](https://nodejs.org/en) or the dependency manager of your choice:

    ```cmd title=""
    npm install
    ```

3. Run the development server:

    ```cmd title=""
    npm run dev
    ```
