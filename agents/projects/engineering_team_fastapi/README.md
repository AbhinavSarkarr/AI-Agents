# Todo App Backend

This is a FastAPI application for a Todo application.

## Requirements
Install the required packages:

```bash
pip install -r requirements.txt
```

## Running the Application
To run the application, use:

```bash
uvicorn main:app --reload
```

## API Endpoints
- POST /api/auth/signup
- POST /api/auth/login
- POST /api/tasks
- GET /api/tasks

## Additional Features
- Advanced filters, pagination, and search on tasks.
- User authentication and authorization via dependencies.
- Integrated logging for better traceability.
- Connection pooling for optimized database access.
- Background tasks and job scheduling in place.
- API versioning and rate limiting for scalability and performance.