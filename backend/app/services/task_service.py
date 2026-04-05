from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import Optional, List
from ..models import Task
from ..schemas import TaskCreate, TaskUpdate, PaginatedTasks

class TaskService:
    @staticmethod
    def get_tasks(
        db: Session,
        user_id: int,
        search: Optional[str] = None,
        completed: Optional[bool] = None,
        priority: Optional[str] = None,
        category_id: Optional[int] = None,
        page: int = 1,
        limit: int = 20,
        sort: str = "task_order",
        order: str = "asc"
    ) -> PaginatedTasks:
        query = db.query(Task).filter(Task.user_id == user_id)
        
        if search:
            query = query.filter(Task.title.ilike(f"%{search}%"))
        if completed is not None:
            query = query.filter(Task.completed == completed)
        if priority:
            query = query.filter(Task.priority == priority)
        if category_id:
            query = query.filter(Task.category_id == category_id)
        
        total = query.count()
        
        sort_column = getattr(Task, sort, Task.task_order)
        if order == "desc":
            query = query.order_by(desc(sort_column))
        else:
            query = query.order_by(sort_column)
        
        tasks = query.offset((page - 1) * limit).limit(limit).all()
        pages = (total + limit - 1) // limit
        
        return PaginatedTasks(
            items=tasks,
            total=total,
            page=page,
            limit=limit,
            pages=pages
        )
    
    @staticmethod
    def create_task(db: Session, user_id: int, task_data: TaskCreate) -> Task:
        max_order = db.query(Task).filter(Task.user_id == user_id).count()
        db_task = Task(
            **task_data.model_dump(),
            user_id=user_id,
            task_order=max_order
        )
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task
    
    @staticmethod
    def get_task(db: Session, task_id: int, user_id: int) -> Optional[Task]:
        return db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
    
    @staticmethod
    def update_task(db: Session, task: Task, task_data: TaskUpdate) -> Task:
        update_data = task_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)
        db.commit()
        db.refresh(task)
        return task
    
    @staticmethod
    def delete_task(db: Session, task: Task) -> None:
        db.delete(task)
        db.commit()
    
    @staticmethod
    def reorder_tasks(db: Session, user_id: int, task_orders: List[dict]) -> List[Task]:
        for item in task_orders:
            task = db.query(Task).filter(
                Task.id == item["task_id"],
                Task.user_id == user_id
            ).first()
            if task:
                task.task_order = item["new_order"]
        db.commit()
        return db.query(Task).filter(Task.user_id == user_id).order_by(Task.task_order).all()
