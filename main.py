from fastapi import FastAPI
import schema

app = FastAPI()

@app.post("/blog")
def create(request: schema.Blog):
    return request
