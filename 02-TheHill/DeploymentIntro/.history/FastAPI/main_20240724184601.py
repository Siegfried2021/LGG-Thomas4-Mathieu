from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class ComputationInput(BaseModel):
    salary: 2000
    bonus: float
    taxes: float

@app.get("/")
def read_root():
    return {"message": "Welcome to the API"}

@app.get("/multiply/{number}")
def multiply_by_two(number: int):
    return {"result": number * 2}

@app.post("/compute")
def compute(input: ComputationInput):
    try:
        result = input.salary + input.bonus - input.taxes
        return {"result": result}
    except ValueError:
        raise HTTPException(status_code=400, detail="expected numbers, got strings.")

@app.exception_handler(ValueError)
async def value_error_exception_handler(request, exc):
    return JSONResponse(status_code=400, content={"error": "expected numbers, got strings."})

@app.exception_handler(KeyError)
async def key_error_exception_handler(request, exc):
    missing_field = exc.args[0]
    return JSONResponse(status_code=400, content={"error": f"3 fields expected (salary, bonus, taxes). You forgot: {missing_field}."})
