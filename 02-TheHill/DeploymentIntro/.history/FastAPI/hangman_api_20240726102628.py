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
        hidden_word = hidden_word,
        lives_left = 6,
        guessed_letters=[]
    )
    games[game_id] = game_state
    return game_state

@app.post("/guess/{game_id}/{letter}", response_model=GameState)
def guess_letter(game_id: int, letter:str):
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Non-existing game")
    
    game_state = games[game_id]
    
    if letter in game_state.guessed_letters:
        raise HTTPException(status_code=400, detail="Letter already guessed")
    
    game_state.guessed_letters.append(letter)
    
    if letter in game_state.secret_word:
        game_state.hidden_word = "".join(
            [letter if game_state.secret_word[i] == letter else game_state.hidden_word[i] for i in range(len(game_state.word))]
        )
        
    
