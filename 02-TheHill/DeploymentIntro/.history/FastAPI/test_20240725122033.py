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
    salary : None
    bonus : None
    taxes = None

@app.post("/compute_salary")
def compute_salary(data: SalaryData):
    missing_fields = 0
    if data.salary is None:
        missing_fields += 1
    if data.bonus is None:
        missing_fields += 1
    if data.taxes is None:
        missing_fields += 1

    if missing_fields > 0:
        raise HTTPException(status_code=400, detail=f"{missing_fields} missing fields. Please provide salary, bonus, and taxes.")

    if float(data.salary) and float(data.bonus) and float(data.taxes):
        result = data.salary + data.bonus - data.taxes
        return {"result": result}
    else:
        raise HTTPException(status_code=400, detail="Invalid input. Please provide numbers for salary, bonus, and taxes.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
