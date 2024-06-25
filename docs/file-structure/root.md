# Root Files

In the root of the `project` there are only three files to worry about.

- `.env.local` - a file for the environment variables (API keys and database url)
- `.gitignore` - the ignore file for GitHub
- `README.md` - a markdown file for explaining what your project is about

```shell title="Project Root"
root
├───backend
│   │   ...
└───frontend
│   │   ...
│   .env.local
│   .gitignore
│   README.md
```

## Environment File

`.env.local` is one of those files you use at the start of your project to configure it and then tweak it again just before deployment.

We've tried to make configuration as easy as possible and added comments in the file with links to each tool so you can start configuring your API keys immediately.

Here's what it looks like:

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

## Gitignore

The `.gitignore` file is used when pushing files to a [GitHub](https://github.com/) repository. Any files or directories defined inside it, are ignored within git commits. This is useful for preventing unnecessary files (such as `node_modules`), or ones that contain sensitive information (such as `.env.local`), from ending up in your repo.

We've preconfigured and tailored the `.gitignore` file to the project already to help you jump straight into project development.

## Readme

The `README.md` acts as the face of your GitHub repository. It's where you put all your information about the project you've created, how to install it and run it, etc.
