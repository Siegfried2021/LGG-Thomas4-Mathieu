import streamlit as st
import requests

# Set the FastAPI endpoint
API_URL = "http://localhost:8000"

# Function to start a new game
def start_new_game():
    response = requests.post(f"{API_URL}/start_game")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to start a new game")
        return None

# Function to make a guess
def make_guess(game_id, letter):
    response = requests.post(f"{API_URL}/guess/{game_id}/{letter}")
    if response.status_code in [200, 400]:
        return response.json()
    else:
        st.error(response.json()["detail"])
        return None

# Function to get game status
def get_game_status(game_id):
    response = requests.get(f"{API_URL}/game_status/{game_id}")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to retrieve game status")
        return None

st.title("Hangman Game")

# Initialize or retrieve game state
if "game_state" not in st.session_state:
    st.session_state.game_state = None
    st.session_state.game_id = None

# Start a new game button
if st.button("Start New Game"):
    game_state = start_new_game()
    if game_state:
        st.session_state.game_state = game_state
        st.session_state.game_id = game_state["game_id"]

# Display game state if available
if st.session_state.game_state:
    game_state = st.session_state.game_state
    st.write(f"Word: {game_state['hidden_word']}")
    st.write(f"Lives Left: {game_state['lives_left']}")
    st.write(f"Guessed Letters: {', '.join(game_state['guessed_letters'])}")

    # Input for guessing a letter
    letter = st.text_input("Guess a letter").lower()
    if st.button("Submit Guess"):
        if letter:
            updated_state = make_guess(st.session_state.game_id, letter)
            if updated_state:
                st.session_state.game_state = updated_state

    # Display endgame messages
    if st.session_state.game_state["lives_left"] == 0:
        st.error("Game Over! The word was: " + st.session_state.game_state["secret_word"])
    elif "_" not in st.session_state.game_state["hidden_word"]:
        st.success("Congratulations! You've found the secret word: " + st.session_state.game_state["secret_word"])
else:
    st.write("Press 'Start New Game' to begin.")