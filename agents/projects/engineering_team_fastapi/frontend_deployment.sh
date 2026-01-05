#!/bin/bash
# React Frontend Build and Deployment Script

# Navigate to the frontend directory
cd frontend

# Install dependencies if necessary
# npm install

# Build the React app
npm run build

# Serve the React app using serve
npm install -g serve
serve -s build -l 3000
