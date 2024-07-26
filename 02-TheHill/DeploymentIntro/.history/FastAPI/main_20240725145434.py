from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ValidationError

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to this cool testing API"}

@app.get("/multiply/{number}")
def multiply_number(number: int):
    return {"result": number * 2}

class SalaryData(BaseModel):
    salary
    bonus: float
    taxes: float

@app.post("/compute_salary")
def compute_salary(data: SalaryData):
    try:
        result = data.salary + data.bonus - data.taxes
        return {"result": result}
    except ValidationError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Validation error: {e.errors()}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid input: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
