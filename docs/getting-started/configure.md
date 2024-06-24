# Configuring The Project


## Getting Started With The Project

We understand that every new project structure can be quite dawnting, especially when you have no idea what each folder represents! To reduce the barrier for using the projects created by this tool we've put together some helpful [documentation](https://create.achronus.dev/).

We strongly recommend you look through it, but it isn't really necessary to get started. Here's a checklist for files to update to be able to start using the project:

- `.env.local` - start by updating your API keys, such as a `DB_URL`
- `backend/app/config/settings.py` - Update the `DB_NAME` and `DB_COLLECTION_NAME` for your MongoDB database
- `backend/app/models/__init__.py` - Update the `ExampleDB` model

That's it! Only three files! Pretty good, right?

### Where To Start?

This typically depends on your experience. If you are more comfortable with `Python` we recommend starting with `FastAPI` (`backend`) and create your routes and models in the `models` and `routers` directories.

However, if you are more familiar with `React` and `NextJS` (`frontend`), start in the `app/layout` to change your `metadata` and the `pages/Homepage` to update the homepage -> `Homepage.tsx`.

Feeling a little overwhelmed? Refer to our [documentation](https://create.achronus.dev/).
