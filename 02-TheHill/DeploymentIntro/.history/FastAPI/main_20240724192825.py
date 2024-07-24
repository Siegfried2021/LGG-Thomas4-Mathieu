from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse

app = FastAPI()

class ComputationInput(BaseModel):
    salary: 150
    bonus: 12
    taxes: int

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
async def value_error_exception_handler():
    return JSONResponse(status_code=400, content={"error": "expected numbers, got strings."})

@app.exception_handler(KeyError)
async def key_error_exception_handler(exc):
    missing_field = exc.args[0]
    return JSONResponse(status_code=400, content={"error": f"3 fields expected (salary, bonus, taxes). You forgot: {missing_field}."})
