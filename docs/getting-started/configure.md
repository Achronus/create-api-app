# Configuring The Project

Each project can be configured in three easy steps:

1. Update your API keys and database URL
2. Update the database details in the `settings.py` file
3. Update the `ExampleDB` model to match your database collection

## Updating Your API Keys

Inside the `root` directory access the `.env.local` file and follow the links to get your API keys. Simply add them at their corresponding location.

The file will look something like this:

!!! note
    Some API keys may be missing depending on the packages you have [`excluded`](installation.md#installation).

```python title=".env.local"
# The URL to connect FastAPI and NextJS together - used in `frontend/next.config.mjs`
FASTAPI_CONNECTION_URL=http://127.0.0.1:8000/

# MongoDB: The connection url to your database
# https://www.mongodb.com/
DB_URL=

# Uploadthing: storing files and handling file uploading
# https://uploadthing.com/
UPLOADTHING_SECRET=
NEXT_PUBLIC_UPLOADTHING_APP_ID=

# Clerk: User Authentication
# https://clerk.com/docs/quickstarts/nextjs
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=
CLERK_SECRET_KEY=

NEXT_PUBLIC_CLERK_SIGN_IN_URL=/auth/sign-in
NEXT_PUBLIC_CLERK_SIGN_UP_URL=/auth/sign-up
NEXT_PUBLIC_CLERK_AFTER_SIGN_IN_URL=/
NEXT_PUBLIC_CLERK_AFTER_SIGN_UP_URL=/

# Stripe: user payments
# https://stripe.com/docs
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=
STRIPE_SECRET_KEY=
STRIPE_WEBHOOK_SECRET=
NEXT_PUBLIC_STRIPE_CLIENT_ID=
NEXT_PUBLIC_PLATFORM_SUBSCRIPTION_PERCENT=1
NEXT_PUBLIC_PLATFORM_ONETIME_FEE=2
NEXT_PUBLIC_PLATFORM_PERCENT=1
NEXT_PRODUCT_ID=
```

## Updating Database Details

Navigate to `backend/app/config/settings.py` and then update the [`DB_NAME`](#updating-database-details) and [`DB_COLLECTION_NAME`](#updating-database-details) to reflect your MongoDB database.

??? tip "Databases and Collections"
    Collections are just a fancy way of saying a `table`. You can read more about them in the [MongoDB documentation](https://www.mongodb.com/docs/manual/core/databases-and-collections/).

```python title="config/settings.py" hl_lines="13-14"
import os

from app.utils.fileloader import FileLoader


class Settings:
    __fileloader = FileLoader()

    DIRPATHS = __fileloader.DIRPATHS
    FILEPATHS = __fileloader.FILEPATHS

    DB_URL = os.getenv("DATABASE_URL")
    DB_NAME = ""  # Update me!
    DB_COLLECTION_NAME = ""  # Update me!


settings = Settings()
```

## Updating The Database Model

Navigate to `backend/app/models/__init__.py` then update the class name `ExampleDB` to one of your choice and update its values.

Here's a before and after for a recent project we did:

??? Tip "New To Pydantic or Beanie?"
    Check out their docs for more information:
    
    - [Pydantic](https://docs.pydantic.dev/)
    - [Beanie](https://beanie-odm.dev/)

=== "Before"

    ```python title="__init__.py"
    from typing import Optional

    from app.config.settings import settings

    from beanie import Document
    from pydantic import BaseModel


    class ExampleDB(Document):
        """
        The main model for your database collection. Should represent the structure of the data in the collection.

        For more details check the [Beanie docs](https://beanie-odm.dev/).
        """

        name: str
        desc: Optional[str] = None

        class Settings:
            name = settings.DB_COLLECTION_NAME


    __beanie_models__ = [ExampleDB]
    ```

=== "After"

    ```python title="__init__.py"
    from typing import Optional

    from app.config.settings import settings

    from beanie import Document
    from pydantic import BaseModel

    # Other Pydantic models
    # ...

    class DBSpellDetails(Document, CoreDetails):
        """The spell detail representation in the database."""

        desc: list[str]
        higher_level: list[str]
        range: str
        components: list[str]
        ritual: bool
        duration: str
        concentration: bool
        casting_time: str
        level: int
        damage: Optional[DamageType] = None
        dc: Optional[DCType] = None
        school: CoreDetails
        classes: list[CoreDetails]
        subclasses: list[CoreDetails]

        class Settings:
            name = settings.DB_SPELLS_COLLECTION


    __beanie_models__ = [DBSpellDetails]
    ```

## Where To Go Next?

Well done for getting this far! :clap:

Deciding where to start with your project typically depends on your experience.

If you are more comfortable with `Python` we recommend starting with the `FastAPI` part of the project in the `backend` directory. Start by creating your routes and models in the `models` and `routers` directories.

More familiar with `React` and `NextJS`? Start with the `frontend` directory, specifically the `metadata` in the `app/layout` and the `Homepage.tsx` in `pages/Homepage`.

We also recommend getting familiar with the project file structure using the links below.

<div class="grid cards" markdown>

-   :simple-nextdotjs:{ .md .middle } __Frontend__

    ---

    Home to the [`Next.js`](#where-to-go-next) files.

    [:octicons-arrow-right-24: Frontend file structure](../file-structure/frontend.md)

-   :simple-fastapi:{ .md .middle } __Backend__

    ---

    Home to the [`FastAPI`](#where-to-go-next) files.

    [:octicons-arrow-right-24: Backend file structure](../file-structure/backend.md)

</div>
