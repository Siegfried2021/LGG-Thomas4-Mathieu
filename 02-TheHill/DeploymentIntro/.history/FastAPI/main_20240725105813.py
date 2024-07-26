from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Welcome to this cool testing API"}

@app.get("/multiply/{number}")
def multiply_number(number: int):
    return {"result": number * 2}

class SalaryData(BaseModel):
    salary: float
    bonus: float
    taxes: float

@app.post("/compute_salary")
def compute_salary(data):
    if 'salary' not in data or 'bonus' not in data or 'taxes' not in data:
        raise HTTPException(status_code=400, detail="Missing fields. Please provide salary, bonus, and taxes.")

    try:
        salary = float(data.salary)
        bonus = float(data.bonus)
        taxes = float(data.taxes)
    except ValueError:
        raise HTTPException(status_code=400,
                            detail="Invalid input. Please provide numbers for salary, bonus, and taxes.")

    result = salary + bonus - taxes
    return {"result": result}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
