# Deployment Instructions

## Local Development Setup

1. **Clone the repository**:
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. **Navigate to backend directory** and deploy:
   ```bash
   cd backend
   chmod +x ../backend_deployment.sh
   ../backend_deployment.sh
   ```

3. **Navigate to frontend directory** and deploy:
   ```bash
   cd frontend
   chmod +x ../frontend_deployment.sh
   ../frontend_deployment.sh
   ```

## Production Setup

1. **Build and run using Docker Compose**:
   ```bash
   docker-compose up --build
   ```

2. **Access the applications**:
   - backend: http://localhost:8000/docs
   - frontend: http://localhost:3000

## Smoke Testing Results
- **All tests passed**. Health check endpoints are functioning as expected.

## Access URLs and API Documentation Links
- Access frontend at: http://localhost:3000
- Access backend api documentation at: http://localhost:8000/docs
