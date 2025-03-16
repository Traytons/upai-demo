from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
import logging

logging.basicConfig(level=logging.INFO)

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True

class LeadCreate(BaseModel):
    estimator_id: int
    contractor_id: int
    client_name: str
    phone: str
    email: str
    status: str = "pending"
    created_at: datetime = Field(default_factory=datetime.utcnow)  # ✅ Fixed!

class LeadBase(BaseModel):
    estimator_id: int
    contractor_id: Optional[int]  # Allow None
    client_name: str
    phone: str
    email: str
    status: str

class LeadResponse(LeadBase):
    id: int
    created_at: str  # Ensure FastAPI receives a string

    class Config:
        from_attributes = True  # Corrected replacement for `orm_mode = True`

    @classmethod
    def from_orm(cls, obj):
        created_at_str = obj.created_at.isoformat() if obj.created_at else "MISSING_TIMESTAMP"
        
        # Debugging Output
        logging.info(f"🚨 Raw created_at: {obj.created_at} | Converted: {created_at_str}")

        return cls(
            id=obj.id,
            estimator_id=obj.estimator_id,
            contractor_id=obj.contractor_id if obj.contractor_id is not None else 0,  
            client_name=obj.client_name,
            phone=obj.phone,
            email=obj.email,
            status=obj.status,
            created_at=created_at_str  # ✅ Convert datetime to ISO string
        )
    
class LeadCreate(LeadBase):
    pass
