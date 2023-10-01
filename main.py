from fastapi import FastAPI
import schema, models
from database import engine

app = FastAPI()

models.Base.metadata.create_all(engine)

@app.post("/blog")
def create(request: schema.Blog):
    return request
