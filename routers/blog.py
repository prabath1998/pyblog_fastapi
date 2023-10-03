from typing import List
from fastapi import APIRouter, Depends, status,Response, HTTPException 
from sqlalchemy.orm import Session

import schema, database, models

router = APIRouter()

# get all blogs
@router.get("/blog", status_code=200,tags=["blogs"])
def get_all(db: Session = Depends(database.get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

# create new blog
@router.post("/blog", status_code=status.HTTP_201_CREATED, tags=["blogs"])
def create(request: schema.Blog, db: Session = Depends(database.get_db)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

# delete blog
@router.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT,tags=["blogs"])
def destroy(id, db: Session = Depends(database.get_db)):
    # db.query(models.Blog).filter(models.Blog.id == id).delete()
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found"
        )
    else:
        blog.delete()
    db.commit()
    return {"Deleted"}


@router.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED,tags=["blogs"])
def update(id, request: schema.Blog, db: Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found"
        )
    else:
        blog.update({"title": request.title, "body": request.body})
    db.commit()
    return "Updated successfully"



# get blog with id
@router.get("/get/{id}", status_code=200, response_model=schema.ShowBlog,tags=["blogs"])
def show(id, response: Response, db: Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with the id {id} not found!",
        )
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail': f"Blog with the id {id} not found!"}
    return blog