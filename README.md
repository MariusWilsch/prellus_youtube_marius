# YouTube Transcript Processor

A simple two-page application for processing YouTube transcripts and generating audio.

## Quick Start

The application can be started in two ways:

### 1. Background Mode (Default)

```bash
./startup.sh
```

This starts both servers in the background and returns control to your terminal. The servers will continue running in the background even after the script completes.

### 2. Foreground Mode (For Debugging)

```bash
./foreground_startup.sh
```

This shows real-time output and keeps your terminal occupied until you press Ctrl+C.

To stop all services when using background mode:

```bash
./shutdown.sh
```

## Client-Friendly Launcher Options

For non-technical users, we provide several simplified launcher options:

### Option 1: One-Click Mac Launch Script

Simply double-click the `launch_app.command` file to start the application. A terminal window will open to show progress, and the application will automatically open in your web browser.

To stop the application, double-click the `stop_app.command` file.

### Option 2: Desktop Application

For the most user-friendly experience, you can use our desktop application launcher:

1. Double-click the YouTube Transcript Processor application icon
2. Click the "Start Application" button
3. When the application is ready, click "Open Application in Browser"
4. Use the application in your web browser
5. When done, click "Stop Application" in the desktop launcher

See [CLIENT_SETUP_GUIDE.md](CLIENT_SETUP_GUIDE.md) for detailed instructions for non-technical users.

## Docker Setup (Recommended)

For a consistent development environment, you can use Docker Compose:

1. Copy the environment variables template:
```bash
cp .env.example .env
```

2. Edit the `.env` file to add your API keys:
```bash
nano .env  # or use any text editor
```

3. Build and start the containers:
```bash
docker-compose up -d
```

4. Stop and remove containers:
```bash
docker-compose down
```

5. View logs:
```bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend
docker-compose logs -f frontend
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:5001

## Important Note About Background Mode

When you run `./startup.sh`, the script will finish and return to the command prompt, but **the application is still running in the background**. This is normal and expected behavior for background processes.

You can verify the application is running with:

```bash
# Check if processes are running
ps -p $(cat .running_pids)

# Check backend connectivity
curl http://localhost:5001/api/test

# View logs in real-time
tail -f backend/port5001_server.log
tail -f frontend/frontend_log.txt
```

See the [Startup Process Documentation](track_and_trace/startup_process.md) for more details.

## Issue Resolution

The application has been updated to use port 5001 instead of 5000, as port 5000 is already in use by macOS Control Center on newer versions of macOS.

## Manual Setup (if needed)

If you need to start the servers manually:

1. Start the backend:
```bash
cd backend
python3 port5001_server.py
```

2. Start the frontend (in a new terminal):
```bash
cd frontend
npm start
```

## Testing the API Directly

You can test the backend API directly using curl:

```bash
curl http://localhost:5001/api/test
```

Or by opening this URL in your browser: http://localhost:5001

## Features

The application consists of:

1. **Input Page**:
   - YouTube URL input
   - Custom processing prompt
   - Duration estimate

2. **Overview Page**:
   - View processed transcripts
   - Generate audio from transcripts
   - Download audio files

## Troubleshooting

If you encounter any issues:

- Run the diagnostic script: `./diagnose.sh`
- Check if port 5001 is already in use: `lsof -i :5001`
- View backend logs: `tail -f backend/port5001_server.log`
- View frontend logs: `tail -f frontend/frontend_log.txt`
- Restart both servers: `./shutdown.sh && ./startup.sh`

### Common Issues and Solutions

1. **"The script finishes but the application doesn't work"**
   - The application runs in the background after the script completes
   - Try checking logs with `tail -f backend/port5001_server.log`
   - Verify processes are running with `ps -p $(cat .running_pids)`

2. **Port 5000 conflicts with macOS services**
   - Solution: We're now using port 5001 instead

3. **Network connection errors**
   - Solution: Check backend logs and ensure the backend is running on port 5001

4. **Frontend can't connect to backend**
   - Solution: Verify the API_URL in `frontend/src/services/api.js` is set to `http://localhost:5001/api`

5. **Docker-related issues**
   - Solution: Try rebuilding the containers with `docker-compose up --build`
   - Check Docker logs with `docker-compose logs -f`

## Technology Stack

- Frontend: React
- Backend: Flask with CORS support
- Communication: RESTful API
- Containerization: Docker and Docker Compose