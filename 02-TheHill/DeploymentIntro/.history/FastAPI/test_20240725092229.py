from fastapi import FastAPI
from pydantic import BaseModel

class Calculation(BaseModel):
    salary
    bonus
    taxes
    
@app.get("/")
def read_root():
    return

@get.multiply("/multiply/{number}")
def multiply_by_two