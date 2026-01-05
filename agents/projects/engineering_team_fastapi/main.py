from fastapi import FastAPI, Depends, HTTPException, Request
from routers import auth, tasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
import logging

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Middleware
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])
app.add_middleware(GZipMiddleware)

# Custom exception handler
@app.exception_handler(Exception)
async def unicorn_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {exc}")
    return JSONResponse(status_code=500, content={"message": "Internal Server Error"})

# Include routers
app.include_router(auth.router)
app.include_router(tasks.router)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Todo App API"}

@app.on_event('startup')
async def startup_event():
    logger.info('Application startup')

@app.on_event('shutdown')
async def shutdown_event():
    logger.info('Application shutdown')