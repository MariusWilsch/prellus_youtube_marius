# YouTube Transcript Processor - Desktop Launcher

This is a simple Electron-based desktop application that serves as a launcher for the YouTube Transcript Processor. It provides a user-friendly interface for non-technical users to start and stop the application.

## Prerequisites

- Node.js 14+ and npm installed
- Docker Desktop installed

## Development Setup

1. Install dependencies:
   ```bash
   cd desktop-launcher
   npm install
   ```

2. Run the app in development mode:
   ```bash
   npm start
   ```

## Building for Distribution

### For macOS:

1. Create the macOS app:
   ```bash
   npm run package-mac
   ```

2. The built application will be in the `dist` folder.

3. For a proper macOS application, you may want to:
   - Sign the application with your Apple Developer ID
   - Create a DMG installer (you can use tools like `create-dmg`)
   - Add icons and proper macOS metadata

### For Windows:

1. Create the Windows app:
   ```bash
   npm run package-win
   ```

2. The built application will be in the `dist` folder.

3. For a proper Windows application, you may want to:
   - Sign the application with a code signing certificate
   - Create an installer (you can use tools like NSIS or Inno Setup)
   - Add icons and proper Windows metadata

## Distribution to Clients

### Simple Method:

1. Build the app for your client's platform (Mac or Windows)
2. Copy the entire application folder to the client's computer
3. Ensure Docker Desktop is installed on the client's machine
4. The client can run the application by clicking on the executable

### Professional Method:

1. Create a proper installer that:
   - Checks for/installs Docker (or prompts the user to install it)
   - Places the app in the proper location
   - Creates desktop shortcuts
   - Registers file associations if needed
   - Sets up auto-updates

2. Distribute the installer to your client

## Notes for Distribution

- Make sure the app can find the docker-compose.yaml file. The app expects to be in a folder that's a sibling to the docker-compose file.
- Ensure that all environment variables are properly set before distributing.
- You may want to include a version of the .env file pre-configured with appropriate API keys for your client. 