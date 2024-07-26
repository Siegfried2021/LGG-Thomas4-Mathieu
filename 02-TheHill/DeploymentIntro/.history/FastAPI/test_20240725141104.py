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
    salary: float
    bonus: float
    taxes: float

@app.post("/compute_salary")
def compute_salary(data: SalaryData):
    if data.salary or data.t

    if missing_fields:
        raise HTTPException(
            status_code=400, 
            detail=f"Missing fields: {', '.join(missing_fields)}. Please provide salary, bonus, and taxes."
        )

    if int(data.salary) and int(data.bonus) and int(data.taxes):
        result = data.salary + data.bonus - data.taxes
        return {"result": result}
    else:
        raise HTTPException(status_code=400, detail="Invalid input. Please provide numbers for salary, bonus, and taxes.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
