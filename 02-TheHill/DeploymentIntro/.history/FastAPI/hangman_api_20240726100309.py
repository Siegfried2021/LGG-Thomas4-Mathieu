from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import random

app = FastAPI()

target_words = ["python", "fastapi", "beautifulsoup", "regression", "pycharm", "pandas", "prediction"]

class GameState(BaseModel):
    word: str
    secret_word: str
    lives_left: int
    
    