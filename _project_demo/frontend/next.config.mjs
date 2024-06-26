/** @type {import('next').NextConfig} */

import path from "path";
import dotenv from "dotenv";
import fs from "fs";

const loadEnv = (filename) => {
  const currentDir = process.cwd();
  const rootDir = path.parse(currentDir).dir;

  const localFile = path.resolve(currentDir, filename);
  const rootFile = path.resolve(rootDir, filename);

  const localExists = fs.existsSync(localFile);
  const rootExists = fs.existsSync(rootFile);

  if (!localExists && !rootExists) {
    throw new Error(
      `Missing environment file: '${filename}'!`
    );
  }

  const filepath = localExists ? localFile : rootFile;

  const env = dotenv.config({ path: filepath });
  return env.parsed;
};

const env = loadEnv(".env.local");
const apiUrl = process.env.FASTAPI_CONNECTION_URL;

const nextConfig = {
  env: env,
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "utfs.io",
        pathname: `/a/${process.env.NEXT_PUBLIC_UPLOADTHING_APP_ID}/*`,
      },
      {
        protocol: "https",
        hostname: apiUrl,
        pathname: `/api/*`,
      },
    ],
  },
  rewrites: async () => {
    return [
      {
        source: "/api/:path*",
        destination: `${apiUrl}/api/:path*`,
      },
      {
        source: "/docs",
        destination: `${apiUrl}/docs`,
      },
      {
        source: "/openapi.json",
        destination: `${apiUrl}/openapi.json`,
      },
    ];
  },
};

export default nextConfig;
