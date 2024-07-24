from fastapi import FastAPI
from pydantic import BaseModel, ValidationError
from fastapi.responses import JSONResponse

app = FastAPI()

class ComputationInput(BaseModel):
    salary: 5000
    bonus: 250
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

