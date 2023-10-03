from typing import List
from fastapi import APIRouter, Depends, status,Response, HTTPException 
from sqlalchemy.orm import Session

import schema, database, models, hashing

router = APIRouter()

# save user with hashed password
@router.post("/user", response_model= schema.ShowUser,tags=["users"])
def create_user(request: schema.User, db: Session = Depends(database.get_db)):
    new_user = models.User(
        name=request.name,
        email=request.email,
        password=hashing.Hash.bcrypt(request.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/user/{id}',response_model=schema.ShowUser,tags=["users"])
def get_user(id:int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with the id {id} not found!",
        )
    return user