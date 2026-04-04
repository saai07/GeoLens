# GeoLens Frontend

This directory contains the frontend portion of the **GeoLens** application. It is built using modern web development tools and frameworks to provide a sleek, performant, and responsive user interface for displaying Generative Engine Optimization (GEO) audit scores and Schema recommendations.

## Tech Stack

The frontend is built with:

- **Framework**: [Next.js](https://nextjs.org/) (App Router format)
- **UI & Components**: [React 19](https://react.dev/)
- **Styling**: [Tailwind CSS v4](https://tailwindcss.com/)
- **Syntax Highlighting**: [`react-syntax-highlighter`](https://github.com/react-syntax-highlighter/react-syntax-highlighter) (for displaying the recommended JSON-LD schemas beautifully)
- **Language**: TypeScript

## Prerequisites

Before running the application, ensure you have the following installed:

- **Node.js** (v20+ recommended)
- **NPM** (comes with Node.js)

## Getting Started

Follow these instructions to set up the frontend locally for development.

### 1. Install Dependencies

Navigate to the `frontend` directory and install the required npm packages:

```bash
cd frontend
npm install
```

### 2. Configure Environment Variables

Create a `.env.local` file in the root of the `frontend` directory. Ensure it matches your backend configuration. 
Example `.env.local`:

```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 3. Run the Development Server

Start the Next.js development server:

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser to view the application.

## Available Scripts

In the project directory, you can run:

- `npm run dev`: Runs the app in the development mode.
- `npm run build`: Builds the app for production to the `.next` folder.
- `npm run start`: Starts the production server using the built application.
- `npm run lint`: Runs ESLint to catch and fix common issues.

## Project Structure

- `src/app/`: Contains the Next.js app router pages, layouts, and global styles.
- `src/components/`: Reusable React components used across pages.

---


