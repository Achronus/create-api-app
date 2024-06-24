# Customization

This section is dedicated to the customization of the project.

## Changing From MongoDB to SQL

This tool doesn't currently support `SQL` databases. If you are looking to use one instead, we recommend checking out FastAPI's great [documentation](https://fastapi.tiangolo.com/tutorial/sql-databases/?h=sql) on the matter.

If you choose this option, you'll need to remove the `beanie` package from the `backend` and update the following files:

- `backend/app/db/__init__.py`
- `backend/app/main.py` - the lifespan method
