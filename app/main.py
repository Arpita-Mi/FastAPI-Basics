from fastapi import FastAPI, Depends, HTTPException 
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import UserCreate, User as UserResponse
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from .service import create_user
# Create the FastAPI instance
app = FastAPI()

# Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

@app.post("/users/", response_model=UserResponse)
async def create_user_api(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user.

    This endpoint allows the client to create a new user by providing 
    user details in the request body. The password will be hashed before 
    storing it in the database.

    Parameters:
    - user: UserCreate - The user details including username and password.
    - db: Session - The database session dependency.

    Returns:
    - UserResponse: The created user object.

    Raises:
    - HTTPException: If there's an error during user creation.
    """
    try:
        new_user = create_user(user, db)
        return new_user
    except Exception as e:
        raise HTTPException(status_code=500 , detail={"message":str(e)})


@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a user by ID.

    This endpoint fetches a user from the database using the provided 
    user ID. If the user does not exist, a 404 error is raised.

    Parameters:
    - user_id: int - The ID of the user to retrieve.
    - db: Session - The database session dependency.

    Returns:
    - UserResponse: The user object corresponding to the provided ID.

    Raises:
    - HTTPException: If the user is not found (404).
    """
    breakpoint()
    print(user_id)
    print(User.id)
    user = db.query(User).filter(User.id == user_id).first()
    print(user)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

