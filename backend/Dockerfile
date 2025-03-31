FROM python:3.9

WORKDIR /app

# Copy requirements.txt first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install additional dependencies for audio processing
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Copy the project
COPY . .

# Set environment variables
ENV PYTHONPATH=/app
ENV FLASK_APP=backend/port5001_server.py
ENV FLASK_ENV=development

# Expose the port the app runs on
EXPOSE 5001

# Command to run the application
CMD ["python", "backend/port5001_server.py"] 