#!/bin/bash

# Make the terminal window more user-friendly
echo "==================================================="
echo "    YouTube Transcript Processor - Shutting Down   "
echo "==================================================="

# Navigate to the app directory
cd "$(dirname "$0")"

# Stop the application
echo "Stopping application..."
docker-compose down

if [ $? -eq 0 ]; then
  echo "Application stopped successfully!"
else
  echo "There was a problem stopping the application."
fi

echo ""
echo "You can close this window now."
echo "==================================================="

# Keep the terminal window open until the user presses a key
echo "Press any key to close this window..."
read -n 1 