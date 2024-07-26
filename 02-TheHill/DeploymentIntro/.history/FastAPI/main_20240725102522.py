from fastapi import FastAPI, Request
from pydantic import BaseModel, Field, field_validator
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


app = FastAPI()
class ComputationInput(BaseModel):
    salary: int = Field(..., description="The salary amount")
    bonus: int = Field(..., description="The bonus amount")
    taxes: int = Field(..., description="The taxes amount")

    @field_validator('salary', 'bonus', 'taxes', mode='before')
    def check_positive(cls, value, field):
        if not isinstance(value, int):
            raise ValueError(f"Field '{field.name}' should be an integer.")
        if value < 0:
            raise ValueError(f"Field '{field.name}' should be a positive integer.")
        return value
    
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "Error": f"3 fields expected (salary, bonus, taxes). You forgot: {field.name}."}),
    )

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