from fastapi import FastAPI, Request
from pydantic import BaseModel, Field, field_validator
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

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

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    error_messages = []
    for error in errors:
        loc = '.'.join(map(str, error['loc']))  # Convert location list to string
        msg = error['msg']
        error_messages.append(f"Field '{loc}' error: {msg}")
    return JSONResponse(
        status_code=400,
        content={"error": " | ".join(error_messages)}
    )

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
