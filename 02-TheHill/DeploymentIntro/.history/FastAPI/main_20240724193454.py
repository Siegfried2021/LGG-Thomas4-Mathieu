from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ComputationInput(BaseModel):
    salary: int
    bonus: int
    taxes: int

@app.get("/")
def read_root():
    return {"message": "Welcome to the API"}

@app.get("/multiply/{number}")
def multiply_by_two(number: int):
    return {"result": number * 2}

@app.post("/compute")
def compute(input: ComputationInput):
        result = input.salary + input.bonus - input.taxes
        return {"result": result}


