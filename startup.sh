#!/bin/bash

# Get script directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

# Make sure ports are free
pkill -f "npm start" > /dev/null 2>&1 || true
pkill -f "python.*port5001" > /dev/null 2>&1 || true
sleep 2

# Create directories
mkdir -p logs

# Start backend
cd "$DIR/backend"
python3 port5001_server.py > "$DIR/logs/backend.log" 2>&1 &
echo "Backend started with PID: $!"
echo "$!" > "$DIR/backend.pid"

# Wait for backend
sleep 5

# Start frontend with BROWSER=none
cd "$DIR/frontend"
export BROWSER=none
npm start > "$DIR/logs/frontend.log" 2>&1 &
echo "Frontend started with PID: $!"
echo "$!" > "$DIR/frontend.pid"

echo
echo "IMPORTANT: DO NOT CLOSE THIS TERMINAL WINDOW"
echo "Both servers are now running."
echo "Open http://localhost:3000 in your browser manually."
echo
echo "To stop the servers, press Ctrl+C in this window."

# Keep this script running to maintain the servers
echo "Monitoring server logs (Ctrl+C to stop)..."
tail -f "$DIR/logs/backend.log" "$DIR/logs/frontend.log"