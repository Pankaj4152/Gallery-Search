# Gallery Search Frontend

This is the React + TypeScript + Vite frontend for the Gallery Search project.

## Getting Started

### 1. Install dependencies

```sh
npm install
```
or
```sh
yarn
```

### 2. Run the development server

```sh
npm run dev
```
or
```sh
yarn dev
```

The app will be available at [http://localhost:5173](http://localhost:5173) by default.

## Features

- User signup and login (JWT authentication)
- Protected routes for authenticated users
- Image gallery, upload, and search interfaces
- API requests handled via Axios with JWT token support

## Project Structure

- `src/` — Main source code
- `src/pages/` — Page components (e.g., Signup, Login, Gallery)
- `src/components/` — Reusable UI components
- `src/api/axiosInstance.ts` — Axios instance with JWT support

## Environment Variables

If you need to configure API endpoints or secrets, create a `.env` file in this directory.

## Build for Production

```sh
npm run build
```
or
```sh
yarn build
```

## Linting

```sh
npm run lint
```
or
```sh
yarn lint
```

---

**Make sure your backend server is running and CORS is enabled for local development.**