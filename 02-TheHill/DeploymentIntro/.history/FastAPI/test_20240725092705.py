from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

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

@post.calculate("/calculate")
def calculate(input: Calculation):
    return input.