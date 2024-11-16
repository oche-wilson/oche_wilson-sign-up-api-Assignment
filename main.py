from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field, EmailStr
from fastapi.middleware.cors import CORSMiddleware
import time

app = FastAPI()

# CORS Middleware to allow only localhost:8000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

# In-memory storage for users
users = []

# Pydantic model for user data validation
class User(BaseModel):
    first_name: str = Field(..., min_length=1)
    last_name: str = Field(..., min_length=1)
    age: int = Field(..., ge=1)
    email: str = Field(...,)
    height: float = Field(..., gt=0)

# Logger middleware to print request time
@app.middleware("http")
async def log_request_time(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f"Request processing time: {process_time:.4f} seconds")
    return response

# Endpoint to create a user
@app.post("/users", status_code=201)
async def create_user(user: User):
    # Check if user with the same email already exists
    if any(u["email"] == user.email for u in users):
        raise HTTPException(status_code=400, detail="User with this email already exists")
    
    # Add user to in-memory storage
    users.append(user.dict())
    return {"message": "User created successfully", "user": user}

