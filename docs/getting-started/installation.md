# Installation

!!! info "Before Starting"

    Make sure you have [`Docker`](https://docs.docker.com/get-docker/) installed. 
    
    We use the [Build NextJS App Tool](https://github.com/Achronus/build-nextjs-app) to create the frontend files which requires [`Docker`](https://docs.docker.com/get-docker/).

1. Install the package through `PIP`:

    ```bash title=""
    pip install create_api_app
    ```

2. Create a new project:

    ```bash title=""
    create-api-app <project_name> # (1)!
    ```

      1. Replace `<project_name>` with the name of your choice!

:sparkles: And that's it! :sparkles:

Once built, you'll find two folders: a [`frontend`](#installation) and a [`backend`](#installation).

<div class="grid cards" markdown>

-   :simple-nextdotjs:{ .md .middle } __Frontend__

    ---

    Home to the [`Next.js`](#installation) files.

    [:octicons-arrow-right-24: Frontend file structure](../file-structure/frontend.md)

-   :simple-fastapi:{ .md .middle } __Backend__

    ---

    Home to the [`FastAPI`](#installation) files.

    [:octicons-arrow-right-24: Backend file structure](../file-structure/backend.md)

</div>
