from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ValidationError
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
    result = data.salary + data.bonus - data.taxes
    return {"result": result}

# Exception handler for invalid data
@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    missing_fields = [e['loc'][0] for e in exc.errors() if e['type'] == 'value_error.missing']
    if missing_fields:
        return JSONResponse(
            status_code=400,
            content={"error": f"3 fields expected (salary, bonus, taxes). You forgot: {', '.join(missing_fields)}."}
        )
    return JSONResponse(
        status_code=400,
        content={"error": "expected numbers, got strings."}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)