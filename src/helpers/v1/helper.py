from fastapi import status,Depends,HTTPException
from src.schemas.v1.user_schema import UserCreate
from sqlalchemy.orm import Session
from src.config.v1.database import get_db
from src.models.v1.user_model import User as UserModel

def validate_unique_email(data : UserCreate, db : Session = Depends(get_db)):
    is_existing_email = db.query(UserModel).filter(UserModel.email == data.email).first()
    
    if is_existing_email:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "Email Already Exist"
        )
    return data

def validate_unique_name(data : UserCreate, db : Session = Depends(get_db)):
    is_existing_name = db.query(UserModel).filter(UserModel.name == data.name).first()
    
    if is_existing_name:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "Name Already Exist"
        )
    return data