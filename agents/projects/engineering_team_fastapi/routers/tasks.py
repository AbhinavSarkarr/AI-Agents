from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models.task import Task
from schemas.task import TaskCreate, TaskResponse
from database import SessionLocal
import logging

router = APIRouter()

# Logging setup
logger = logging.getLogger(__name__)

# Dependency to get DB session

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.remove()

@router.post("/tasks", response_model=TaskResponse)
async def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    db_task = Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    logger.info(f"Task created: {db_task.title}")
    return db_task

@router.get("/tasks")
async def read_tasks(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    tasks = db.query(Task).offset(skip).limit(limit).all()
    logger.info(f"Retrieved {len(tasks)} tasks")
    return tasks
