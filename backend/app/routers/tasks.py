from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from ..database import get_db
from ..models import User
from ..schemas import TaskCreate, TaskUpdate, TaskResponse, TaskReorder, PaginatedTasks
from ..services import TaskService
from ..utils.dependencies import get_current_user

router = APIRouter(prefix="/api/tasks", tags=["Tasks"])

@router.get("", response_model=PaginatedTasks)
def get_tasks(
    search: Optional[str] = Query(None),
    completed: Optional[bool] = Query(None),
    priority: Optional[str] = Query(None),
    category_id: Optional[int] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    sort: str = Query("task_order"),
    order: str = Query("asc"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return TaskService.get_tasks(
        db, current_user.id, search, completed, priority, category_id, page, limit, sort, order
    )

@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return TaskService.create_task(db, current_user.id, task_data)

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = TaskService.get_task(db, task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = TaskService.get_task(db, task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return TaskService.update_task(db, task, task_data)

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = TaskService.get_task(db, task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    TaskService.delete_task(db, task)

@router.patch("/reorder", response_model=List[TaskResponse])
def reorder_tasks(
    task_orders: List[TaskReorder],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return TaskService.reorder_tasks(
        db, current_user.id, [{"task_id": t.task_id, "new_order": t.new_order} for t in task_orders]
    )
