from typing import List
from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from repository import user
import schema, database, models, hashing

router = APIRouter(prefix="/user", tags=["users"])


# save user with hashed password
@router.post("/", response_model=schema.ShowUser)
def create_user(request: schema.User, db: Session = Depends(database.get_db)):
    return user.create(request, db)


@router.get("/{id}", response_model=schema.ShowUser)
def get_user(id: int, db: Session = Depends(database.get_db)):
    return user.show(id, db)
