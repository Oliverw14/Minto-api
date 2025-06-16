import select
from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta
import jwt
import bcrypt
import os

from models import (
    User, 
    db_session_maker
)

auth_router = APIRouter(prefix="/auth", tags=["authentication"])

# Security configuration
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Pydantic models
class LoginRequest(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# TODO: Replace with actual database
# This is a mock user store - replace with your database
fake_users_db = {
    "user@example.com": {
        "email": "user@example.com",
        "hashed_password": bcrypt.hashpw("password123".encode('utf-8'), bcrypt.gensalt()),
        "full_name": "Test User",
        "disabled": False
    }
}

def verify_password(plain_password: str, hashed_password: bytes) -> bool:
    """Verify a password against its hash."""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def authenticate_user(email: str, password: str):
    """Authenticate a user by email and password."""
    # TODO: Replace with actual database query
    user = fake_users_db.get(email)
    if not user:
        return False
    if not verify_password(password, user["hashed_password"]):
        return False
    return user

@auth_router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Login endpoint that accepts email/username and password.
    Returns a JWT access token on successful authentication.
    """
    # OAuth2PasswordRequestForm uses 'username' field, but we can treat it as email
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"]}, expires_delta=access_token_expires
    )
    
    return JSONResponse(
        status_code=200,
        content={
            "success": 1,
            "access_token": access_token,
            "token_type": "bearer"
        }
    )
@auth_router.post("/login/json")
async def login_json(login_data: LoginRequest):
    """
    Alternative login endpoint that accepts JSON payload.
    Returns a JWT access token on successful authentication.
    """
    user = authenticate_user(login_data.email, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"]}, expires_delta=access_token_expires
    )
    
    return JSONResponse(
        status_code=200,
        content={
            "access_token": access_token,
            "token_type": "bearer",
            "success": 1,
            "message": "Login successful"
        }
    )

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Dependency to get the current authenticated user from JWT token.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except jwt.PyJWTError:
        raise credentials_exception
    
    # TODO: Replace with actual database query
    user = fake_users_db.get(token_data.email)
    if user is None:
        raise credentials_exception
    
    return user

@auth_router.get("/me")
async def read_users_me(current_user: dict = Depends(get_current_user)):
    """
    Get current user information.
    Requires authentication.
    """
    return JSONResponse(
        status_code=200,
        content={
            "email": current_user["email"],
            "full_name": current_user["full_name"],
            "disabled": current_user["disabled"],
            "success": 1
        }
    )


@auth_router.post('/verification-email')
def send_verification_email(email: str = Form(...)):
    # Your logic to send verification email goes here
    with db_session_maker() as cursor:
        stmt = select(
            User
        ).where(
            User.ena
        )
    
    return {"success": 1, "message": f"Verification email sent to {email}"}
