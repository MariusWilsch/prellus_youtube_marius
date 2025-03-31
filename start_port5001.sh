#!/bin/bash

# Colors for better output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== YouTube Transcript Processor - Port 5001 Edition ===${NC}"

# Stop any existing processes
echo -e "${YELLOW}Stopping any running servers...${NC}"
pkill -f "npm start" > /dev/null 2>&1 || true
pkill -f "python.*port5001_server.py" > /dev/null 2>&1 || true
pkill -f "python.*simple_backend.py" > /dev/null 2>&1 || true
pkill -f "python.*app.py" > /dev/null 2>&1 || true
sleep 1

# Check Python installation
echo -e "${YELLOW}Checking Python installation...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python3 is not installed. Please install it first.${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python3 is installed${NC}"

# Check Node installation
echo -e "${YELLOW}Checking Node.js installation...${NC}"
if ! command -v node &> /dev/null; then
    echo -e "${RED}Node.js is not installed. Please install it first.${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Node.js is installed: $(node --version)${NC}"

# Check if port 5001 is already in use
echo -e "${YELLOW}Checking if port 5001 is available...${NC}"
if lsof -Pi :5001 -sTCP:LISTEN -t >/dev/null ; then
    echo -e "${RED}Port 5001 is already in use. Please free this port first.${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Port 5001 is available${NC}"

# Install backend dependencies
echo -e "${YELLOW}Installing backend dependencies...${NC}"
cd backend
if [ -f "requirements.txt" ]; then
    python3 -m pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo -e "${RED}Failed to install backend dependencies${NC}"
        exit 1
    fi
    echo -e "${GREEN}✓ Backend dependencies installed${NC}"
else
    echo -e "${YELLOW}requirements.txt not found, installing minimal dependencies...${NC}"
    python3 -m pip install flask flask-cors
    echo -e "${GREEN}✓ Minimal Flask dependencies installed${NC}"
fi

# Start the port 5001 backend
echo -e "${YELLOW}Starting Flask backend server on port 5001...${NC}"
python3 port5001_server.py > port5001_server.log 2>&1 &
BACKEND_PID=$!
echo -e "${GREEN}✓ Backend started with PID: $BACKEND_PID${NC}"

# Wait for backend to start
echo -e "${YELLOW}Waiting for backend to start...${NC}"
sleep 2

# Test if backend is running
echo -e "${YELLOW}Testing backend connection...${NC}"
curl -s http://localhost:5001/api/test > /dev/null
if [ $? -ne 0 ]; then
    echo -e "${RED}Backend does not seem to be running correctly.${NC}"
    echo -e "${YELLOW}Checking backend logs:${NC}"
    cat port5001_server.log
    exit 1
fi
echo -e "${GREEN}✓ Backend is running correctly at http://localhost:5001${NC}"

# Start the frontend
echo -e "${YELLOW}Starting React frontend server...${NC}"
cd ../frontend
npm start > frontend_log.txt 2>&1 &
FRONTEND_PID=$!
echo -e "${GREEN}✓ Frontend started with PID: $FRONTEND_PID${NC}"

echo -e "\n${GREEN}==================== STARTUP COMPLETE ====================${NC}"
echo -e "${GREEN}Backend:${NC} http://localhost:5001"
echo -e "${GREEN}Frontend:${NC} http://localhost:3000"
echo -e ""
echo -e "${YELLOW}Testing the API directly:${NC}"
curl -X GET http://localhost:5001/api/test
echo -e "\n"
echo -e "${YELLOW}To stop the servers, run:${NC} kill $BACKEND_PID $FRONTEND_PID"
echo -e "${YELLOW}To view backend logs:${NC} tail -f backend/port5001_server.log"
echo -e "${YELLOW}To view frontend logs:${NC} tail -f frontend/frontend_log.txt"
echo -e "${GREEN}===========================================================${NC}" 