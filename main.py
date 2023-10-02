from typing import List
from fastapi import FastAPI, Depends, status, Response, HTTPException
import schema, models, hashing
from database import engine, SessionLocal
from sqlalchemy.orm import Session


app = FastAPI()

models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# create new blog
@app.post("/blog", status_code=status.HTTP_201_CREATED, tags=["blogs"])
def create(request: schema.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


# delete blog
@app.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT,tags=["blogs"])
def destroy(id, db: Session = Depends(get_db)):
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


@app.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED,tags=["blogs"])
def update(id, request: schema.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found"
        )
    else:
        blog.update({"title": request.title, "body": request.body})
    db.commit()
    return "Updated successfully"


# get all blogs
@app.get("/blog", status_code=200, response_model=List[schema.show_blog],tags=["blogs"])
def get_all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


# get blog with id
@app.get("/get/{id}", status_code=200, response_model=schema.show_blog,tags=["blogs"])
def show(id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with the id {id} not found!",
        )
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail': f"Blog with the id {id} not found!"}
    return blog

# save user with hashed password
@app.post("/user", response_model= schema.show_user,tags=["users"])
def create_user(request: schema.User, db: Session = Depends(get_db)):
    new_user = models.User(
        name=request.name,
        email=request.email,
        password=hashing.Hash.bcrypt(request.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get('/user/{id}',response_model=schema.show_user,tags=["users"])
def get_user(id:int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with the id {id} not found!",
        )
    return user
    
