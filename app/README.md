# YouTube Transcript Processor Backend

Simple Flask backend that receives YouTube transcript processing requests from the frontend.

## Setup

1. Install dependencies:
```
pip install -r requirements.txt
```

2. Run the Flask server:
```
python app.py
```

The server will start on http://localhost:5000.

## API Endpoints

### Process Transcript
- URL: `/api/transcripts/process`
- Method: `POST`
- Request Body:
  ```json
  {
    "url": "https://www.youtube.com/watch?v=abc123",
    "prompt": "Custom processing instructions",
    "duration": 30
  }
  ```
- Response:
  ```json
  {
    "id": "transcript_1623432532",
    "title": "Video from abc123",
    "status": "processing",
    "message": "Transcript processing started"
  }
  ```

### Get Transcripts
- URL: `/api/transcripts`
- Method: `GET`
- Response: List of transcript objects

### Generate Audio
- URL: `/api/audio/generate/{transcript_id}`
- Method: `POST`
- Response: Audio generation result

## Notes

This is a simple mock implementation that just receives and prints the inputs.
In a real application, this would connect to the YouTube transcript processing system. 