import streamlit as st
import random

# Target words
target_words = ["python", "fastapi", "beautifulsoup", "regression", "pycharm", "pandas", "prediction", "unicorn"]

# Initialize session state
if 'secret_word' not in st.session_state:
    st.session_state.secret_word = ''
if 'hidden_word' not in st.session_state:
    st.session_state.hidden_word = ''
if 'lives_left' not in st.session_state:
    st.session_state.lives_left = 6
if 'guessed_letters' not in st.session_state:
    st.session_state.guessed_letters = []

def start_game():
    st.session_state.secret_word = random.choice(target_words)
    st.session_state.hidden_word = "_" * len(st.session_state.secret_word)
    st.session_state.lives_left = 6
    st.session_state.guessed_letters = []

def guess_letter(letter):
    if letter in st.session_state.guessed_letters:
        st.warning("Letter already guessed")
        return
    st.session_state.guessed_letters.append(letter)
    if letter in st.session_state.secret_word:
        st.session_state.hidden_word = "".join(
            [letter if st.session_state.secret_word[i] == letter else st.session_state.hidden_word[i] for i in range(len(st.session_state.secret_word))]
        )
    else:
        st.session_state.lives_left -= 1
    if st.session_state.lives_left == 0:
        st.error(f"Game over! The secret word was: {st.session_state.secret_word}")
        start_game()
    if "_" not in st.session_state.hidden_word:
        st.success(f"Congratulations! You've found the secret word: {st.session_state.secret_word}")

# Streamlit UI
st.title("Hangman Game")

if st.button('Start New Game'):
    start_game()

if st.session_state.secret_word:
    st.write(f"Secret word: {st.session_state.hidden_word}")
    st.write(f"Lives left: {st.session_state.lives_left}")
    st.write(f"Guessed letters: {', '.join(st.session_state.guessed_letters)}")

    guess = st.text_input("Enter a letter").lower()
    if st.button('Guess') and guess:
        guess_letter(guess)
        st.experimental_rerun()