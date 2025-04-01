# DevOps Guide

## Prerequisites
- Docker
- Make
- [Nixpacks](https://nixpacks.com/docs/install)

## Quick Start
```bash
# Build both services
make build-all

# Run everything
make run-all

# Check logs
make logs

# Stop everything
make stop-all
```

## Service URLs
- Frontend: http://localhost:3000
- Backend: http://localhost:5001
- Backend Test: http://localhost:5001/api/test

## Common Issues
1. If images fail to run, check they're built for the right platform:
   - Backend needs `linux/amd64`
   - Frontend runs on your native platform

## Clean Up
```bash
make clean  # Removes all containers and images
``` 