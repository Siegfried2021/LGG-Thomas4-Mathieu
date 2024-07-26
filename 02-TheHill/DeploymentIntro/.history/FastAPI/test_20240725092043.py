from fastapi import FastAPI
from pydantic import BaseModel

class Calculation(BaseModel):
    salary
    bonus
    taxes
    
@app.get("/")
def read_root