# Transcript Automation Frontend

This is the frontend application for the Transcript Automation System. It provides a user-friendly interface to interact with the transcript processing, analysis, and audio generation capabilities of the backend system.

## Directory Structure

```
frontend/
├── public/             # Static files
├── src/                # Source code
│   ├── assets/         # Images, styles and other assets
│   │   ├── images/     # Image files
│   │   └── styles/     # CSS files
│   ├── components/     # Reusable React components
│   │   └── layout/     # Layout components (Navbar, Footer, etc.)
│   ├── pages/          # Page components for each route
│   ├── services/       # API services for backend communication
│   └── utils/          # Utility functions and helpers
├── package.json        # Dependencies and scripts
└── README.md           # This documentation file
```

## Features

- Process new transcripts from YouTube URLs
- View list of processed transcripts
- View detailed transcript information
- Generate audio from processed transcripts
- Configure TTS settings (voice, language, speed)

## Available Scripts

In the project directory, you can run:

### `npm start`

Runs the app in development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

### `npm test`

Launches the test runner in the interactive watch mode.

### `npm run build`

Builds the app for production to the `build` folder.

## Backend Communication

The application communicates with the backend API using axios. During development, API requests are proxied to `http://localhost:5000` as configured in the `package.json`.

## Adding Components

When adding new components or pages:

1. Create a new file in the appropriate directory (`components/` or `pages/`)
2. Import the component in `App.js` if it's a page, or in the relevant parent component
3. Add a route in `App.js` if it's a page

## API Services

API communication is organized in the `services/` directory. Add new API methods to the relevant service file as needed.

## Styling

The application uses plain CSS with a simple organization:
- Global styles in `src/assets/styles/index.css`
- Component-specific styles should be added as needed 