from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import secrets
from ..models import User
from ..schemas import UserCreate, Token
from ..utils.security import verify_password, get_password_hash, create_access_token

class AuthService:
    @staticmethod
    def get_user_by_email(db: Session, email: str):
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def create_user(db: Session, user_data: UserCreate) -> User:
        hashed_password = get_password_hash(user_data.password)
        db_user = User(
            email=user_data.email,
            password_hash=hashed_password
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> User:
        user = AuthService.get_user_by_email(db, email)
        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user
    
    @staticmethod
    def create_token(user: User) -> Token:
        access_token = create_access_token(data={"sub": str(user.id)})
        return Token(access_token=access_token)
    
    @staticmethod
    def generate_reset_token(db: Session, user: User) -> str:
        # Generate a secure random token
        reset_token = secrets.token_urlsafe(32)
        
        # Store token hash in user (we'll add this field to the model)
        user.reset_token = reset_token
        user.reset_token_exp = datetime.utcnow() + timedelta(hours=1)
        db.commit()
        
        return reset_token
    
    @staticmethod
    def reset_password(db: Session, token: str, new_password: str) -> bool:
        user = db.query(User).filter(User.reset_token == token).first()
        
        if not user:
            return False
        
        # Check if token is expired
        if user.reset_token_exp and user.reset_token_exp < datetime.utcnow():
            # Clear expired token
            user.reset_token = None
            user.reset_token_exp = None
            db.commit()
            return False
        
        # Update password
        user.password_hash = get_password_hash(new_password)
        
        # Clear reset token
        user.reset_token = None
        user.reset_token_exp = None
        
        db.commit()
        return True
