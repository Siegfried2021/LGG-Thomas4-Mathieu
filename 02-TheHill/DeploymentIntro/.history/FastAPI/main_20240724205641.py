from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ValidationError, validator
from fastapi.responses import JSONResponse
from typing import Optional

app = FastAPI()

class ComputationInput(BaseModel):
    salary: Optional[int]
    bonus: Optional[int]
    taxes: Optional[int]

    @validator('salary', 'bonus', 'taxes', always=True)
    def check_not_none(cls, value, field):
        if value is None:
            raise ValueError(f"Field '{field.name}' is required.")
        return value

    @validator('salary', 'bonus', 'taxes')
    def check_type(cls, value, field):
        if not isinstance(value, int):
            raise ValueError(f"Field '{field.name}' should be an integer.")
        return value

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
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    errors = exc.errors()
    error_messages = []
    for error in errors:
        loc = '.'.join(error['loc'])
        msg = error['msg']
        error_messages.append(f"Field '{loc}' error: {msg}")
    return JSONResponse(
        status_code=400,
        content={"error": " | ".join(error_messages)}
    )

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)