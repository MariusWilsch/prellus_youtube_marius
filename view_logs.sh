#!/bin/bash

# Make the terminal window more user-friendly
echo "==================================================="
echo "     YouTube Transcript Processor - View Logs      "
echo "==================================================="
echo "Press Ctrl+C to exit log view"
echo "==================================================="
echo ""

# Navigate to the app directory
cd "$(dirname "$0")"

# Display logs with timestamps
docker-compose logs -f --tail=100 