#!/bin/bash

# Colors for better output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}=== YouTube Transcript Processor - Shutdown Script ===${NC}"

# Check if PID file exists
if [ -f ".running_pids" ]; then
    # Read PIDs and resources from file
    read BACKEND_PID FRONTEND_PID TEE_PID FRONTEND_TEE_PID BACKEND_FIFO FRONTEND_FIFO < .running_pids
    echo -e "${YELLOW}Found stored PIDs and resources${NC}"
    
    # Kill each PID
    for PID in $BACKEND_PID $FRONTEND_PID $TEE_PID $FRONTEND_TEE_PID; do
        if [ -n "$PID" ] && [ "$PID" != "" ]; then
            if ps -p $PID > /dev/null 2>&1; then
                echo -e "${YELLOW}Stopping process with PID $PID...${NC}"
                kill $PID 2>/dev/null || kill -9 $PID 2>/dev/null
            else
                echo -e "${RED}Process with PID $PID is not running${NC}"
            fi
        fi
    done
    
    # Clean up named pipes
    for FIFO in $BACKEND_FIFO $FRONTEND_FIFO; do
        if [ -n "$FIFO" ] && [ "$FIFO" != "" ] && [ -p "$FIFO" ]; then
            echo -e "${YELLOW}Removing named pipe: $FIFO${NC}"
            rm -f "$FIFO"
        fi
    done
    
    # Remove PID file
    rm .running_pids
    echo -e "${GREEN}✓ Cleaned up all resources${NC}"
else
    echo -e "${YELLOW}No stored PIDs found. Using alternative method...${NC}"
fi

# Alternative method - kill processes by name
echo -e "${YELLOW}Stopping any remaining server processes...${NC}"
pkill -f "npm start" >/dev/null 2>&1 || true
pkill -f "node.*start.js" >/dev/null 2>&1 || true
pkill -f "python.*port5001_server.py" >/dev/null 2>&1 || true
pkill -f "python.*simple_backend.py" >/dev/null 2>&1 || true
pkill -f "python.*app.py" >/dev/null 2>&1 || true
pkill -f "python.*minimal_test.py" >/dev/null 2>&1 || true
pkill -f "tee .*backend/port5001_server.log" >/dev/null 2>&1 || true
pkill -f "tee .*frontend/frontend_log.txt" >/dev/null 2>&1 || true

# Wait a moment for processes to terminate
sleep 1

# Check if any processes are still using our ports
echo -e "${YELLOW}Checking if ports are still in use...${NC}"

# Function to check if a port is in use
check_port() {
    local port=$1
    if command -v lsof >/dev/null 2>&1; then
        if lsof -i :$port >/dev/null 2>&1; then
            echo -e "${RED}Port $port is still in use. Trying to force close...${NC}"
            lsof -ti :$port | xargs kill -9 2>/dev/null || true
        else
            echo -e "${GREEN}Port $port is free${NC}"
        fi
    else
        echo -e "${YELLOW}lsof not found, skipping port check for $port${NC}"
    fi
}

# Check our ports
check_port 5001
check_port 3000

# Clean up any remaining pipes
for pipe in /tmp/backend_fifo.* /tmp/frontend_fifo.*; do
    if [ -p "$pipe" ]; then
        echo -e "${YELLOW}Cleaning up named pipe: $pipe${NC}"
        rm -f "$pipe"
    fi
done

echo -e "${GREEN}=== Shutdown complete ===${NC}"
echo -e "${GREEN}You can start the application again by running: ./startup.sh${NC}" 