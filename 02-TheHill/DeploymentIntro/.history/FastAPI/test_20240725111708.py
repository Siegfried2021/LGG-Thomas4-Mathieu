from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to this cool testing API"}

@app.get("/multiply/{number}")
def multiply_number(number: int):
    return {"result": number * 2}

class SalaryData(BaseModel):
    salary: Optional[int]
    bonus: Optional[int]
    taxes: Optional[int]

@app.post("/compute_salary")
def compute_salary(data: SalaryData):
    missing_fields = []
    if data.salary is None:
        missing_fields.append("salary")
    if data.bonus is None:
        missing_fields.append("bonus")
    if data.taxes is None:
        missing_fields.append("taxes")

    if missing_fields:
        raise HTTPException(status_code=400, detail=f"Missing fields: {', '.join(missing_fields)}")

    # Convert to float and compute result
    try:
        salary = float(data.salary)
        bonus = float(data.bonus)
        taxes = float(data.taxes)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid input. Please provide numbers for salary, bonus, and taxes.")

    result = salary + bonus - taxes
    return {"result": result}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
