from fastapi import FastAPI, HTTPException
from fastapi.exceptions import
from pydantic import BaseModel

app = FastAPI()

class Calculation(BaseModel):
    salary: int
    bonus: int
    taxes: int
    
@app.get("/")
def read_root():
    return

@app.get("/multiply/{number}")
def multiply_by_two(number: int):
    return {"result": number * 2}

@app.post("/calculate")
def calculate(input: Calculation):
    try:
        result = input.salary + input.bonus - input.taxes
        return {"result" : result}
    except RequestValidationError as e:
        raise HTTPException(status_code=400, detail=e.errors())