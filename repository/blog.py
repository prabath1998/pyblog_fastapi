from fastapi import Depends, status, HTTPException
from sqlalchemy.orm import Session

import schema, database, models


def get_all(db: Session = Depends(database.get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


def create(request: schema.Blog, db: Session = Depends(database.get_db)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


def delete(id: int, db: Session = Depends(database.get_db)):
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


def update(id: int, request: schema.Blog, db: Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found"
        )
    else:
        blog.update({"title": request.title, "body": request.body})
    db.commit()
    return "Updated successfully"


def show(id: int, db: Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with the id {id} not found!",
        )
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail': f"Blog with the id {id} not found!"}
    return blog
