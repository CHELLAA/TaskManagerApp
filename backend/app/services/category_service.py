from sqlalchemy.orm import Session
from typing import Optional, List
from ..models import Category
from ..schemas import CategoryCreate, CategoryUpdate

class CategoryService:
    @staticmethod
    def get_categories(db: Session, user_id: int) -> List[Category]:
        return db.query(Category).filter(Category.user_id == user_id).all()
    
    @staticmethod
    def create_category(db: Session, user_id: int, category_data: CategoryCreate) -> Category:
        db_category = Category(
            **category_data.model_dump(),
            user_id=user_id
        )
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return db_category
    
    @staticmethod
    def get_category(db: Session, category_id: int, user_id: int) -> Optional[Category]:
        return db.query(Category).filter(
            Category.id == category_id,
            Category.user_id == user_id
        ).first()
    
    @staticmethod
    def update_category(db: Session, category: Category, category_data: CategoryUpdate) -> Category:
        update_data = category_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(category, field, value)
        db.commit()
        db.refresh(category)
        return category
    
    @staticmethod
    def delete_category(db: Session, category: Category) -> None:
        db.delete(category)
        db.commit()
