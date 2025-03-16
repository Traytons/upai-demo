from sqlalchemy.orm import Session
import models, auth, schemas 
from schemas import UserCreate, LeadCreate
import config
from jose import jwt, JWTError
from models import User  # Make sure you have this import
from auth import verify_password  # This should be in auth.py
from sqlalchemy.orm import Session
from datetime import datetime
from auth import hash_password 

def get_leads_by_estimator(db: Session, estimator_id: int):
    leads = db.query(models.Lead).filter(models.Lead.estimator_id == estimator_id).all()
    
    # Convert created_at to string and handle None values
    for lead in leads:
        if lead.contractor_id is None:
            lead.contractor_id = 0  # Default value
        if lead.created_at:
            lead.created_at = lead.created_at.strftime("%Y-%m-%d %H:%M:%S")

    return leads

def get_user_from_token(token: str, db: Session):
    """Retrieves user from token"""
    print(f"Decoding Token: {token}")  # Debugging print statement

    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        print(f"Decoded Token Payload: {payload}")  # Debugging print statement

        username = payload.get("sub")
        if username is None:
            print("No username found in token")
            return None

        user = db.query(models.User).filter(models.User.username == username).first()
        if user:
            print(f"User found: {user.username}")
        else:
            print("User not found in database")

        return user
    except JWTError as e:
        print(f"JWT Error: {e}")
        return None

# Create a new user
def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = hash_password(user.password)  # Hash the password
    db_user = models.User(username=user.username, email=user.email, password_hash=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Get user by username
def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

# Create a new lead
def create_lead(db: Session, lead: schemas.LeadCreate):
    db_lead = models.Lead(
        estimator_id=lead.estimator_id,
        contractor_id=lead.contractor_id,
        client_name=lead.client_name,
        phone=lead.phone,
        email=lead.email,
        status=lead.status
    )
    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)
    return db_lead

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.password_hash):
        return None
    return user

def get_leads_by_contractor(db: Session, contractor_id: int):
    return db.query(models.Lead).filter(models.Lead.contractor_id == contractor_id).all()

def get_lead_response(lead):
    return {
        "id": lead.id,
        "estimator_id": lead.estimator_id,
        "contractor_id": lead.contractor_id,
        "client_name": lead.client_name,
        "phone": lead.phone,
        "email": lead.email,
        "status": lead.status,
        "created_at": lead.created_at.strftime("%Y-%m-%d %H:%M:%S")  # Convert datetime to string
    }