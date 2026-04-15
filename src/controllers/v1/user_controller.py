from fastapi import APIRouter,status,Depends,HTTPException,Query
from src.schemas.v1.user_schema import UserCreate,UserResponse
from sqlalchemy.orm import Session
from src.config.v1.database import get_db
from src.models.v1.user_model import User as UserModel
from src.helpers.v1.helper import validate_unique_email
from typing import Annotated
from src.filters.v1.user_filter import UserFilters

router = APIRouter()

#Create
@router.post("/", response_model=UserResponse, status_code = status.HTTP_201_CREATED)
def create_user(data : UserCreate = Depends(validate_unique_email), db : Session = Depends(get_db)): 
    try:
        user = UserModel(
            name = data.name,
            email = data.email,
            password = data.password
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail= f"Error = {str(error)}"
        )


#Read user
@router.get("/", response_model=list[UserResponse], status_code=status.HTTP_200_OK)
def read_user(filters : Annotated[UserFilters,Query()], db : Session = Depends(get_db)):
    user = db.query(UserModel)
    
    if filters.name:
        user = user.filter(UserModel.name.like(f"%{filters.name}%"))

    if filters.email:
        user = user.filter(UserModel.email.like(f"%{filters.email}%"))
        
    return user.all()

#Read specific user
@router.get("/{id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def read_specific_user(id : int, db : Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == id).first()
    if not user:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Data not found"
        )
    return user


#Delete user
@router.delete("/{id}", status_code = status.HTTP_200_OK)
def delete_user(id:int, db:Session = Depends(get_db)):
    try:
        user = db.query(UserModel).filter(UserModel.id == id).one()
        db.delete(user)
        db.commit()
        return{"status" : "user successfully delete"}
    except Exception as error:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"error : {str(error)}" 
        )
    




    