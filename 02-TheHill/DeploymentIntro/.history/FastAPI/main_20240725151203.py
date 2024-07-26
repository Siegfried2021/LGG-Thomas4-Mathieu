from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, root_validator, ValidationError

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to this cool testing API"}

@app.get("/multiply/{number}")
def multiply_number(number: int):
    return {"result": number * 2}

class SalaryData(BaseModel):
    salary : object
    bonus : object
    taxes : object
    @root_validator
    def check_all_fields_present(cls, values):
        missing_fields = [field for field in ["salary", "bonus", "taxes"] if values.get(field) is None]
        if missing_fields:
            raise ValueError(f"3 fields expected (salary, bonus, taxes). You forgot: {missing_fields}.")
        return values

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
