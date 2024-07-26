from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

# Route that handles GET request
@app.get("/")
def read_root():
    return {"message": "Welcome to the API"}

# Route that handles POST request
@app.post("/")
def post_root(data: Dict[str, str]):
    return {"message": "You posted", "data": data}

# Route that takes a number in the request and returns this number multiplied by 2
@app.get("/multiply/{number}")
def multiply_by_two(number: int):
    return {"result": number * 2}

# Data model for the salary computation
class SalaryData(BaseModel):
    salary: float
    bonus: float
    taxes: float

# POST route that takes a dictionary and returns the computation of salary + bonus - taxes
@app.post("/compute")
def compute_salary(data: SalaryData):
    try:
        result = data.salary + data.bonus - data.taxes
        return {"result": result}
    except ValueError:
        raise HTTPException(status_code=400, detail="expected numbers, got strings.")

# Exception handler for missing fields
@app.exception_handler(ValueError)
def value_error_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={"error": str(exc)}
    )

@app.exception_handler(KeyError)
def key_error_handler(request, exc):
    missing_field = exc.args[0]
    return JSONResponse(
        status_code=400,
        content={"error": f"3 fields expected (salary, bonus, taxes). You forgot: {missing_field}."}
    )
