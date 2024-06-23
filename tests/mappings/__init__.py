TOML_DESCRIPTION = [
    "[tool.poetry]\n",
    'name = "app"\n',
    'version = "0.1.0"\n',
    'description = "A FastAPI backend for processing API data and passing it to the frontend."\n',
    'authors = ["Ryan Partridge <rpartridge101@gmail.com>"]\n',
    'readme = "README.md"\n',
    "\n",
    "[tool.poetry.scripts]\n",
    'run = "build:start"\n',
    "\n",
]

FRONTEND_ROOT_FILES = [
    ".eslintrc.json",
    ".gitignore",  # Cleanup
    "bun.lockb",  # Cleanup
    "components.json",
    "next-env.d.ts",
    "next.config.mjs",
    "package.json",
    "postcss.config.mjs",
    "public\\next.svg",
    "public\\vercel.svg",
    "public",
    "README.md",  # Cleanup
    "src\\app",
    "src\\components",
    "src\\data",
    "src\\hooks",
    "src\\layouts",
    "src\\lib",
    "src\\pages",
    "src\\types",
    "src",
    "tailwind.config.ts",
    "tsconfig.json",
]
