from typing import Annotated

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from api.user_management import models
from api.user_management import schemas
from api.token.main import verify_password, create_access_token, get_current_user, get_password_hash
from api.user_management.schemas import LoginResponse
from database.database import get_db

router = APIRouter(prefix='/user', tags=['Users'], responses={400: {'description': 'Bad Request'}})


@router.post('/create', response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(name=user.name, email=user.email, hashed_password=get_password_hash(user.password))
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=LoginResponse)
def user_login(user: schemas.Login, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user is None:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    db_user.token_info = create_access_token(data={"sub": db_user.name})
    return db_user


@router.get("/{user_id}", response_model=schemas.User)
def get_user_detail(current_user: Annotated[schemas.User, Depends(get_current_user)],
                    ):
    return current_user
