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
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'guess' not in st.session_state:
    st.session_state.guess = ''
if 'warning_message' not in st.session_state:
    st.session_state.warning_message = ''

def start_game():
    st.session_state.secret_word = random.choice(target_words)
    st.session_state.hidden_word = "_" * len(st.session_state.secret_word)
    st.session_state.lives_left = 6
    st.session_state.guessed_letters = []
    st.session_state.game_over = False
    st.session_state.guess = ''
    st.session_state.warning_message = ''

def guess_letter(letter):
    if letter in st.session_state.guessed_letters:
        st.session_state.warning_message = "Letter already guessed"
        return
    st.session_state.guessed_letters.append(letter)
    st.session_state.warning_message = ''  # Clear any previous warning message
    if letter in st.session_state.secret_word:
        st.session_state.hidden_word = "".join(
            [letter if st.session_state.secret_word[i] == letter else st.session_state.hidden_word[i] for i in range(len(st.session_state.secret_word))]
        )
    else:
        st.session_state.lives_left -= 1
    if st.session_state.lives_left == 0:
        st.session_state.game_over = True
        st.error(f"Game over! The secret word was: {st.session_state.secret_word}")
    if "_" not in st.session_state.hidden_word:
        st.session_state.game_over = True
        st.success(f"Congratulations! You've found the secret word: {st.session_state.secret_word}")

st.title("Hangman Game")

if st.button('Start New Game'):
    start_game()

if st.session_state.secret_word:
    st.write(f"Secret word: {st.session_state.hidden_word}")
    st.write(f"Lives left: {st.session_state.lives_left}")
    st.write(f"Guessed letters: {', '.join(st.session_state.guessed_letters)}")

    if st.session_state.warning_message:
        st.warning(st.session_state.warning_message)

    if not st.session_state.game_over:
        guess = st.text_input("Enter a letter", key="guess_input").lower()
        if st.button('Guess'):
            guess_letter(guess)
            st.session_state.guess = '' 
            st.experimental_rerun()
    else:
        if st.session_state.lives_left == 0:
            st.error(f"Game over! The secret word was: {st.session_state.secret_word}")
        else:
            st.success(f"Congratulations! You've found the secret word: {st.session_state.secret_word}")