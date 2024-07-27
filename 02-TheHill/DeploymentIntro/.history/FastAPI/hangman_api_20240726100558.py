from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import random

app = FastAPI()

target_words = ["python", "fastapi", "beautifulsoup", "regression", "pycharm", "pandas", "prediction"]

class GameState(BaseModel):
    secret_word: str
    hidden_word: str
    lives_left: int
    guessed_letters: List[str]
    
games: {}

@app.post("/start_game", response_model=GameState)
def start_game():    
    word = random.choice(target_words)
    secret_word = "_" * len(word)
    