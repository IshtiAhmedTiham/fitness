from fastapi import APIRouter,status,Depends,HTTPException
from src.schemas.v1.user_schema import UserCreate,UserResponse
from sqlalchemy.orm import Session
from src.config.v1.database import get_db
from src.models.v1.user_model import User as UserModel

router = APIRouter()

#Create
@router.post("/", response_model=UserResponse,status_code=status.HTTP_201_CREATED)
def create_user(data : UserCreate, db : Session = Depends(get_db)):
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
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= f"Error = {str(error)}"
        )


#Read user
@router.get("/", response_model=list[UserResponse], status_code=status.HTTP_200_OK)
def read_user(db : Session = Depends(get_db)):
    user = db.query(UserModel).all()
    return user

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
    




    