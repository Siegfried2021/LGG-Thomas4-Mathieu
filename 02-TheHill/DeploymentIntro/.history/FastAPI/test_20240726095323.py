from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import random

app = FastAPI()

# Word list for the Hangman game
WORDS = ["python", "fastapi", "hangman", "openai", "pycharm"]

class GameState(BaseModel):
    word: str
    masked_word: str
    attempts_left: int
    guessed_letters: List[str]

games = {}

@app.post("/start_game", response_model=GameState)
def start_game():
    word = random.choice(WORDS)
    masked_word = "_" * len(word)
    game_id = len(games) + 1
    game_state = GameState(
        word=word,
        masked_word=masked_word,
        attempts_left=6,
        guessed_letters=[]
    )
    games[game_id] = game_state
    return game_state

@app.post("/guess/{game_id}/{letter}", response_model=GameState)
def guess_letter(game_id: int, letter: str):
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")

    game_state = games[game_id]

    if letter in game_state.guessed_letters:
        raise HTTPException(status_code=400, detail="Letter already guessed")

    game_state.guessed_letters.append(letter)

    if letter in game_state.word:
        game_state.masked_word = "".join(
            [letter if game_state.word[i] == letter else game_state.masked_word[i] for i in range(len(game_state.word))]
        )
    else:
        game_state.attempts_left -= 1

    if game_state.attempts_left == 0:
        raise HTTPException(status_code=400, detail="Game over! The word was: " + game_state.word)

    if "_" not in game_state.masked_word:
        raise HTTPException(status_code=200, detail="Congratulations! You've guessed the word: " + game_state.word)

    return game_state

@app.get("/game_status/{game_id}", response_model=GameState)
def game_status(game_id: int):
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")

    return games[game_id]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
