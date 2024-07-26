from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import random

app = FastAPI()

WORDS = ["python", "fastapi", "beautifulsoup", "regression", "pycharm", "pandas", "prediction"]