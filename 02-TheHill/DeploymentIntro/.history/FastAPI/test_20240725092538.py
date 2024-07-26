from fastapi import FastAPI
from pydantic import BaseModel

app = Fa

class Calculation(BaseModel):
    salary
    bonus
    taxes
    
@app.get("/")
def read_root():
    return

@app.get("/multiply/{number}")
def multiply_by_two(number: int):
    return {"result": number * 2}

@post.