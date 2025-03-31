#!/bin/bash

# Colors for better output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== YouTube Transcript Processor - Startup Script ===${NC}"

# Stop any existing processes
echo -e "${YELLOW}Stopping any running servers...${NC}"
pkill -f "npm start" > /dev/null 2>&1 || true
pkill -f "python app.py" > /dev/null 2>&1 || true
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

# Install backend dependencies
echo -e "${YELLOW}Installing backend dependencies...${NC}"
cd backend
python3 -m pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to install backend dependencies${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Backend dependencies installed${NC}"

# Verify Flask app
if [ ! -f "app.py" ]; then
    echo -e "${RED}app.py not found in backend directory${NC}"
    exit 1
fi

# Fix any permission issues
echo -e "${YELLOW}Setting proper permissions...${NC}"
chmod 644 app.py

# Create a new version of the Flask application with simplest possible configuration
echo -e "${YELLOW}Creating simplified Flask app version...${NC}"
cat > simple_app.py << EOL
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/transcripts/process', methods=['POST'])
def process_transcript():
    data = request.json
    print("\n\n===== RECEIVED TRANSCRIPT PROCESSING REQUEST =====")
    print(f"URL: {data.get('url', 'not provided')}")
    print(f"Prompt: {data.get('prompt', 'not provided')}")
    print(f"Duration: {data.get('duration', 'not provided')} minutes")
    print("====================================================\n")
    
    return jsonify({
        'id': '123',
        'title': 'Test Video',
        'status': 'processing',
        'message': 'Request received successfully'
    })

@app.route('/api/transcripts', methods=['GET'])
def get_transcripts():
    return jsonify([
        {
            'id': '1',
            'title': 'Test Transcript',
            'url': 'https://www.youtube.com/watch?v=123',
            'createdAt': '2023-05-20',
            'status': 'completed',
            'audioStatus': None
        }
    ])

@app.route('/api/test', methods=['GET'])
def test():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    print("Starting simplified Flask server on http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
EOL

# Start the backend in a separate terminal
echo -e "${YELLOW}Starting Flask backend server...${NC}"
python3 simple_app.py > backend_log.txt 2>&1 &
BACKEND_PID=$!
echo -e "${GREEN}✓ Backend started with PID: $BACKEND_PID${NC}"

# Wait for backend to start
echo -e "${YELLOW}Waiting for backend to start...${NC}"
sleep 2

# Test if backend is running
echo -e "${YELLOW}Testing backend connection...${NC}"
curl -s http://localhost:5000/api/test > /dev/null
if [ $? -ne 0 ]; then
    echo -e "${RED}Backend does not seem to be running correctly.${NC}"
    echo -e "${YELLOW}Checking backend logs:${NC}"
    cat backend_log.txt
    exit 1
fi
echo -e "${GREEN}✓ Backend is running correctly${NC}"

# Create a simplified API service for the frontend
echo -e "${YELLOW}Updating frontend API service...${NC}"
cd ../frontend
mkdir -p temp

cat > temp/simple_api.js << EOL
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:5000/api',
  headers: {
    'Content-Type': 'application/json',
  }
});

export const transcriptService = {
  processTranscript: async (data) => {
    const response = await api.post('/transcripts/process', data);
    return response.data;
  },
  
  getTranscripts: async () => {
    const response = await api.get('/transcripts');
    return response.data;
  }
};

export const audioService = {
  generateAudio: async (transcriptId) => {
    const response = await api.post(\`/audio/generate/\${transcriptId}\`);
    return response.data;
  }
};

export default api;
EOL

# Copy simplified API if src directory exists
if [ -d "src/services" ]; then
    cp temp/simple_api.js src/services/api.js
    echo -e "${GREEN}✓ Frontend API service updated${NC}"
else
    echo -e "${RED}Cannot find src/services directory in frontend${NC}"
    exit 1
fi

# Start the frontend
echo -e "${YELLOW}Starting React frontend server...${NC}"
npm start > frontend_log.txt 2>&1 &
FRONTEND_PID=$!
echo -e "${GREEN}✓ Frontend started with PID: $FRONTEND_PID${NC}"

echo -e "\n${GREEN}==================== STARTUP COMPLETE ====================${NC}"
echo -e "${GREEN}Backend:${NC} http://localhost:5000"
echo -e "${GREEN}Frontend:${NC} http://localhost:3000"
echo -e ""
echo -e "${YELLOW}Testing the API directly:${NC}"
curl -X GET http://localhost:5000/api/test
echo -e "\n"
echo -e "${YELLOW}To stop the servers, run:${NC} kill $BACKEND_PID $FRONTEND_PID"
echo -e "${YELLOW}To view backend logs:${NC} tail -f backend_log.txt"
echo -e "${YELLOW}To view frontend logs:${NC} tail -f frontend_log.txt"
echo -e "${GREEN}===========================================================${NC}" 