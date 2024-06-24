# Removing Unwanted Packages

Sometimes you might create a project where you don't want or need to use:

- [Clerk](#removing-unwanted-packages) <!-- omit in toc -->
- [Stripe](#removing-unwanted-packages)
- [Uploadthing](#removing-unwanted-packages)

While we haven't integrated this directly into the tool, you can manually remove the ones you don't want. This is a pretty simple process and only requires a few modifications.

## API Keys

Open the [`.env.local`](#api-keys) file in the project directory and remove any API key values associated to the packages you don't want.

```python title=".venv.local" hl_lines="8-11 13-21 23-32"
# The URL to connect FastAPI and NextJS together used in `frontend/next.config.mjs`
FASTAPI_CONNECTION_URL=http://127.0.0.1:8000/

# MongoDB: The connection url to your database
# https://www.mongodb.com/
DB_URL=

# Uploadthing: storing files and handling file uploading
# https://uploadthing.com/
UPLOADTHING_SECRET= # (1)!
NEXT_PUBLIC_UPLOADTHING_APP_ID=

# Clerk: User Authentication
# https://clerk.com/docs/quickstarts/nextjs
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=
CLERK_SECRET_KEY=

NEXT_PUBLIC_CLERK_SIGN_IN_URL=/auth/sign-in # (2)!
NEXT_PUBLIC_CLERK_SIGN_UP_URL=/auth/sign-up
NEXT_PUBLIC_CLERK_AFTER_SIGN_IN_URL=/
NEXT_PUBLIC_CLERK_AFTER_SIGN_UP_URL=/

# Stripe: user payments
# https://stripe.com/docs
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=
STRIPE_SECRET_KEY=
STRIPE_WEBHOOK_SECRET=
NEXT_PUBLIC_STRIPE_CLIENT_ID= # (3)!
NEXT_PUBLIC_PLATFORM_SUBSCRIPTION_PERCENT=1
NEXT_PUBLIC_PLATFORM_ONETIME_FEE=2
NEXT_PUBLIC_PLATFORM_PERCENT=1
NEXT_PRODUCT_ID=
```

1. Remove these lines for [`uploadthing`](#api-keys)
2. Remove these lines for [`clerk`](#api-keys)
3. Remove these lines for [`stripe`](#api-keys)

## Package Dependencies

Next up is the [`package.json`](#package-dependencies) in the [`frontend`](#package-dependencies) directory.

!!! note
    You may see some variations for your [`package.json`](#package-dependencies) but the packages to remove will remain the same!

```json title="package.json" hl_lines="12 14-15 26-27"
{
  "name": "frontend",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  },
  "dependencies": {
    "@clerk/nextjs": "^5.1.6", // (1)!
    "@radix-ui/react-icons": "^1.3.0",
    "@stripe/react-stripe-js": "^2.7.1", // (2)!
    "@stripe/stripe-js": "^4.0.0",
    "class-variance-authority": "^0.7.0",
    "clsx": "^2.1.1",
    "dotenv": "^16.4.5",
    "dotenv-expand": "^11.0.6",
    "lucide-react": "^0.396.0",
    "next": "14.2.4",
    "react": "^18",
    "react-dom": "^18",
    "tailwind-merge": "^2.3.0",
    "tailwindcss-animate": "^1.0.7",
    "@uploadthing/react": "^6.6.0", // (3)!
    "uploadthing": "^6.12.0"
  },
  "devDependencies": {
    "typescript": "^5",
    "@types/node": "^20",
    "@types/react": "^18",
    "@types/react-dom": "^18",
    "postcss": "^8",
    "tailwindcss": "^3.4.1",
    "eslint": "^8",
    "eslint-config-next": "14.2.4"
  }
}
```

1. Remove these lines for [`clerk`](#package-dependencies)
2. Remove these lines for [`stripe`](#package-dependencies)
3. Remove these lines for [`uploadthing`](#package-dependencies)

## Uploadthing Extras

We also added extra functionality to make it easier to work with [`uploadthing`](#uploadthing-extras) so they'll need to remove those files too! They are all located in the [`frontend`](#uploadthing-extras) directory:

```bash title="Truncated Frontend Directory" hl_lines="5-7 13"
└───frontend
    ├───public
    └───src
        ├───app
        │   └───api # (1)!
        │       └───uploadthing
        │           └───list-files
        │ ...
        ├───components
        ├───data
        ├───hooks
        │   └───useFetchData.tsx
        │   └───useFetchImgs.tsx # (2)!
        │   └───useUpdateQueryString.tsx
        ├───layouts
        ├───lib
        ├───pages
        └───types
```

1. Remove the whole [`api`](#uploadthing-extras) directory
2. Remove the [`useFetchImgs.tsx`](#uploadthing-extras) hook

## Future Development

In a future version we will add this functionality automatically.
