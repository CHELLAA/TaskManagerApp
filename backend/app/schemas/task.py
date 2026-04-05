from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    priority: str = "medium"
    due_date: Optional[datetime] = None
    category_id: Optional[int] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[str] = None
    due_date: Optional[datetime] = None
    category_id: Optional[int] = None

class TaskReorder(BaseModel):
    task_id: int
    new_order: int

class CategorySimple(BaseModel):
    id: int
    name: str
    color: str
    
    class Config:
        from_attributes = True

class TaskResponse(TaskBase):
    id: int
    completed: bool
    task_order: int
    user_id: int
    category: Optional[CategorySimple] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class PaginatedTasks(BaseModel):
    items: List[TaskResponse]
    total: int
    page: int
    limit: int
    pages: int
