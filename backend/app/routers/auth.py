from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import UserCreate, UserLogin, UserResponse, Token
from ..services import AuthService
from ..utils.dependencies import get_current_user
from ..models import User

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

class MessageResponse(BaseModel):
    message: str

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = AuthService.get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    return AuthService.create_user(db, user_data)

@router.post("/login", response_model=Token)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = AuthService.authenticate_user(db, user_data.email, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    return AuthService.create_token(user)

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/forgot-password", response_model=MessageResponse)
def forgot_password(request: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = AuthService.get_user_by_email(db, request.email)
    
    # Generate reset token (in production, send email)
    if user:
        reset_token = AuthService.generate_reset_token(db, user)
        # In production, you would send an email here
        # For now, we'll log it (check server console)
        print(f"\n🔑 Password reset link: http://localhost:8000/?reset_token={reset_token}\n")
    
    # Always return success to prevent email enumeration
    return MessageResponse(message="If an account with that email exists, we have sent a password reset link.")

@router.post("/reset-password", response_model=MessageResponse)
def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    success = AuthService.reset_password(db, request.token, request.new_password)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token"
        )
    
    return MessageResponse(message="Password has been reset successfully.")
