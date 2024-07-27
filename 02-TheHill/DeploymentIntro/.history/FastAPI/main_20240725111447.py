from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to this cool testing API"}

@app.get("/multiply/{number}")
def multiply_number(number: int):
    return {"result": number * 2}

class SalaryData(BaseModel):
    salary: int
    bonus: int
    taxes: int

@app.post("/compute_salary")
def compute_salary(data: SalaryData):
    if data.salary not in data or data.bonus not in data or data.taxes not in data:
         raise HTTPException(status_code=400, detail="Missing fields. Please provide salary, bonus, and taxes.")
    try:
        result = data.salary + data.bonus - data.taxes
    except ValueError:
        raise HTTPException(status_code=400,
                            detail="Invalid input. Please provide numbers for salary, bonus, and taxes.")
    return {"result": result}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)