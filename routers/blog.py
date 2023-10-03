from typing import List
from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session

import schema, database, models
from repository import blog

router = APIRouter(prefix="/blog", tags=["blogs"])


# get all blogs
@router.get("/", status_code=200,response_model=List[schema.ShowBlog])
def get_all(db: Session = Depends(database.get_db)):
    return blog.get_all(db)


# create new blog
@router.post("/", status_code=status.HTTP_201_CREATED)
def create(request: schema.Blog, db: Session = Depends(database.get_db)):
    return blog.create(request, db)


# delete blog
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db: Session = Depends(database.get_db)):
    return blog.delete(id, db)


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schema.Blog, db: Session = Depends(database.get_db)):
    return blog.update(id, request, db)


# get blog with id
@router.get("/get/{id}", status_code=200)
def show(id, response: Response, db: Session = Depends(database.get_db)):
    return blog.show(id, db)

#  response_model=schema.ShowBlog