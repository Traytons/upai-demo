from fastapi import APIRouter, Depends, HTTPException, Security, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import models, schemas, auth, crud, config
from database import get_db
from datetime import timedelta
from auth import create_access_token, hash_password
from models import User
from schemas import UserCreate, UserResponse
from crud import create_user

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login/")

@router.get("/", response_model=list[schemas.LeadResponse])
def get_user_leads(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Retrieves all leads for the logged-in user.
    """
    user = crud.get_user_from_token(token, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    return crud.get_leads_by_estimator(db, user.id)

@router.get("/me", tags=["users"])
def read_users_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    print(f"Received Token: {token}")  # Debugging print statement

    user = crud.get_user_from_token(token, db)
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid authentication")

    return user

@router.post("/login")
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid username or password")

    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username})  # ✅ Issue access token

    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = hash_password(user.password)
    new_user = User(username=user.username, email=user.email, password_hash=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully"}