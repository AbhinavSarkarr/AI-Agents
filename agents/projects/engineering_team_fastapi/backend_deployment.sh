#!/bin/bash
# FastAPI Backend Deployment Script

# Activate virtual environment if necessary
# source venv/bin/activate

# Start FastAPI server with uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
