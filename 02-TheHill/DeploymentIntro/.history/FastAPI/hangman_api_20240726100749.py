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
    secret_word = random.choice(target_words)
    hidden_word = "_" * len(secret_word)
    game_id = len(games) + 1
    game_state = GameState(
        secret_word = secret_word,
        hidden_word = hidd
    )
    