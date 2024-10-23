from fastapi import FastAPI, Depends, HTTPException 
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserResponse
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.service import CrudOperations
from utils.utils import logger
# Create the FastAPI instance
app = FastAPI()


@app.post("/create_user/", response_model=dict)
async def create_user_api(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user.
    """
    try:
        crud = CrudOperations(db)
        new_user = crud.create_user(user)
        logger.info("User created successfully.")
        return {"message": "New User Created Successfully"}
    except HTTPException as http_exc:
        logger.warning(f"HTTPException: {http_exc.detail}")
        raise http_exc
    except Exception as e:
        logger.error(f"Failed to create user: {str(e)}")
        raise HTTPException(status_code=500, detail={"message": str(e)})

@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user_api(user_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a user by ID.
    """
    try:
        logger.info(f"Fetching user with ID: {user_id}")
        crud = CrudOperations(db)
        user_detail = crud.get_user(user_id)
        logger.info(f"User retrieved successfully: {user_detail}")
        return user_detail
    except HTTPException as http_exc:
        logger.warning(f"HTTPException: {http_exc.detail}")
        raise http_exc
    except Exception as e:
        logger.error(f"Failed to retrieve user: {str(e)}")
        raise HTTPException(status_code=500, detail={"message": str(e)})

@app.put("/update_user/{user_id}", response_model=UserResponse)
async def update_user_api(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    """
    Update a user by ID.
    """
    try:
        logger.info(f"Attempting to update user with ID: {user_id}")
        crud = CrudOperations(db)
        user_update = crud.update_user(user_id, user)
        logger.info(f"User with ID {user_id} updated successfully.")
        return user_update
    except HTTPException as http_exc:
        logger.warning(f"HTTPException: {http_exc.detail}")
        raise http_exc
    except Exception as e:
        logger.error(f"Failed to update user: {str(e)}")
        raise HTTPException(status_code=500, detail={"message": str(e)})

@app.delete("/delete_user/{user_id}", response_model=dict)
async def delete_user_api(user_id: int, db: Session = Depends(get_db)):
    """
    Delete a user by ID.
    """
    try:
        logger.info(f"Attempting to delete user with ID: {user_id}")
        crud = CrudOperations(db)
        user_delete = crud.delete_user(user_id)  
        return {"message": "User deleted successfully"}
    except HTTPException as http_exc:
        logger.warning(f"HTTPException: {http_exc.detail}")
        raise http_exc
    except Exception as e:
        logger.error(f"Failed to delete user: {str(e)}")
        raise HTTPException(status_code=500, detail={"message": str(e)})
