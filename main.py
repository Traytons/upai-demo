from fastapi import FastAPI, Depends, Security
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
import models
from database import engine
from routes import users, leads

# Define OAuth2 security scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login/")

# Create FastAPI app with authentication setup
app = FastAPI(
    title="Up AI Follow-Up App",
    description="API for managing follow-up leads and users",
    version="1.0.0",
    openapi_tags=[
        {"name": "users", "description": "User-related operations"},
        {"name": "leads", "description": "Lead-related operations"},
    ],
    docs_url="/docs",
    openapi_url="/openapi.json",
)

# Define global security for Swagger
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(leads.router, prefix="/leads", tags=["leads"])

# Create database tables
models.Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Up AI backend is running!"}