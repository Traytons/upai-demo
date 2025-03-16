from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.security import OAuth2PasswordBearer  # ✅ ADD THIS LINE
from sqlalchemy.orm import Session
from database import get_db
import models, schemas, crud
from auth import token_required  # Import the token middleware

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login/")

@router.get("/", response_model=list[schemas.LeadResponse])
def get_user_leads(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
    status: str = Query(None, description="Filter by lead status")  # Add status filter
):
    """Retrieves all leads for the logged-in user, with optional status filtering."""
    
    user = crud.get_user_from_token(token, db)
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid authentication")
    
    # Get all leads assigned to this estimator
    leads_query = db.query(models.Lead).filter(models.Lead.estimator_id == user.id)
    
    if status:  # Apply filter if status is provided
        leads_query = leads_query.filter(models.Lead.status == status)

    return leads_query.all()

@router.post("/", response_model=schemas.LeadResponse)
def create_lead(lead: schemas.LeadCreate, db: Session = Depends(get_db)):
    db_lead = crud.create_lead(db=db, lead=lead)
    return schemas.LeadResponse.from_orm(db_lead)  # Converts ORM model to Pydantic response

@router.get("/contractor/{contractor_id}", response_model=list[schemas.LeadResponse])
def get_leads_by_contractor(contractor_id: int, db: Session = Depends(get_db)):
    """Retrieves all leads for a specific contractor."""
    return crud.get_leads_by_contractor(db, contractor_id)