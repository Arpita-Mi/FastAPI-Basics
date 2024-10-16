from fastapi import FastAPI, Depends, HTTPException 
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserResponse
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.service import CrudOperations

# Create the FastAPI instance
app = FastAPI()

@app.post("/users/", response_model=dict)
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
    - UserResponse: Successfully created message
    Raises:
    - HTTPException: If there's an error during user creation.
    """

    try:
        crud = CrudOperations(db)
        new_user = crud.create_user(user)
        return {"message" : "New User Created Successfully"}
    except Exception as e:
        raise e
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
    
    try:
        crud = CrudOperations(db)
        user_detail = CrudOperations.get_user(user_id)
        return user_detail
    except Exception as e: 
        raise HTTPException(status_code=500 , detail={"message":str(e)})
    

@app.put("/update_users/{user_id}",response_model=UserResponse)
async def update_user_api(user_id : int, user:UserCreate, db:Session=Depends(get_db) ):
    """
    Update a user by ID.

    This endpoint allows to update the details based on the details 
    of user fetched from given user Id and password will be hashed and saved 

    Parameters:
    - user_id: int - The ID of the user to retrieve.
    - user: UserCreate - The user details including username and password.
    - db: Session - The database session dependency.

    Returns:
    - UserResponse: The updated user object.

    Raises:
    - HTTPException: If the user is not found (404).
    """
    try:
        crud = CrudOperations(db)
        user_update = crud.update_user(user_id , user)
        return user_update
    except Exception as e:
        raise HTTPException(status_code=500 , detail={"message":str(e)})
    

@app.delete("/delete_user/{user_id}", response_model=dict)
async def delete_user_api(user_id: int, db:Session=Depends(get_db)):
    """
    Delete a user by ID.

    This endpoint deletes the user by provided user Id

    Parameters:
    - user_id: int - The ID of the user to retrieve.
    - db: Session - The database session dependency.

    Returns:
    - UserResponse: Successfully deleted message

    Raises:
    - HTTPException: If the user is not found (404).
    """
    try:
        crud = CrudOperations(db)
        user_delete = crud.update_user(user_id)
        return {"message":"user deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500 , detail={"message":str(e)})

