#!/bin/bash

# Make the terminal window more user-friendly
echo "==================================================="
echo "    YouTube Transcript Processor - Starting Up     "
echo "==================================================="

# Navigate to the app directory
cd "$(dirname "$0")"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
  echo "Docker is not running! Starting Docker..."
  open -a Docker
  
  # Wait for Docker to start
  echo "Waiting for Docker to start (this may take a minute)..."
  while ! docker info > /dev/null 2>&1; do
    sleep 2
  done
  echo "Docker is now running."
fi

# Check if containers are already running
if docker-compose ps | grep -q "backend.*Up"; then
  echo "Application is already running!"
else
  # Start the application with Docker Compose
  echo "Starting application containers..."
  docker-compose up -d
  
  if [ $? -eq 0 ]; then
    echo "Application started successfully!"
  else
    echo "There was a problem starting the application."
    echo "Press any key to exit."
    read -n 1
    exit 1
  fi
fi

# Wait for services to be ready
echo "Waiting for services to start..."
sleep 5

# Open the browser
echo "Opening application in browser..."
open "http://localhost:3000"

echo ""
echo "==================================================="
echo "  Application is now running in your web browser   "
echo "==================================================="
echo "  • To view logs, run: ./view_logs.sh              "
echo "  • To stop the app, run: ./stop_app.command       "
echo "===================================================" 