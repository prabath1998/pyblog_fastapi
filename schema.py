from pydantic import BaseModel
from typing import List


class Blog(BaseModel):
    title: str
    body: str


class User(BaseModel):
    name: str
    email: str
    password: str


class show_user(BaseModel):
    name: str
    email: str
    blogs: List[Blog] = []

    class Config:
        orm_mode = True

class show_blog(BaseModel):
    title: str
    body: str
    creator: show_user

    class Config:
        orm_mode = True