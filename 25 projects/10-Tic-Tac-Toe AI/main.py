import streamlit as st
import numpy as np

# Initialize session state for game
if 'board' not in st.session_state:
    st.session_state.board = np.full((3, 3), ' ')
    st.session_state.current_player = 'X'
    st.session_state.game_over = False
    st.session_state.winner = None

def check_winner(board, player):
    # Check rows, columns, and diagonals
    for i in range(3):
        if all(board[i, :] == player) or all(board[:, i] == player):
            return True
    if all(board.diagonal() == player) or all(np.fliplr(board).diagonal() == player):
        return True
    return False

def is_board_full(board):
    return not any(' ' in row for row in board)

def minimax(board, depth, is_maximizing):
    if check_winner(board, 'O'):
        return 1
    if check_winner(board, 'X'):
        return -1
    if is_board_full(board):
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'O'
                    score = minimax(board, depth + 1, False)
                    board[i][j] = ' '
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'X'
                    score = minimax(board, depth + 1, True)
                    board[i][j] = ' '
                    best_score = min(score, best_score)
        return best_score

def ai_move():
    best_score = -float('inf')
    best_move = None
    for i in range(3):
        for j in range(3):
            if st.session_state.board[i][j] == ' ':
                st.session_state.board[i][j] = 'O'
                score = minimax(st.session_state.board, 0, False)
                st.session_state.board[i][j] = ' '
                if score > best_score:
                    best_score = score
                    best_move = (i, j)
    if best_move:
        st.session_state.board[best_move[0]][best_move[1]] = 'O'
        st.session_state.current_player = 'X'
        check_game_status()

def check_game_status():
    if check_winner(st.session_state.board, 'X'):
        st.session_state.game_over = True
        st.session_state.winner = 'X'
    elif check_winner(st.session_state.board, 'O'):
        st.session_state.game_over = True
        st.session_state.winner = 'O'
    elif is_board_full(st.session_state.board):
        st.session_state.game_over = True
        st.session_state.winner = 'Draw'

def reset_game():
    st.session_state.board = np.full((3, 3), ' ')
    st.session_state.current_player = 'X'
    st.session_state.game_over = False
    st.session_state.winner = None

# Streamlit UI
st.title("Tic-Tac-Toe with Unbeatable AI")
st.write("Play as X against the AI (O). The AI uses the minimax algorithm to never lose!")

# Display game board
for i in range(3):
    cols = st.columns(3)
    for j in range(3):
        with cols[j]:
            if st.session_state.board[i][j] == ' ' and not st.session_state.game_over:
                if st.button(" ", key=f"{i}{j}"):
                    if st.session_state.current_player == 'X':
                        st.session_state.board[i][j] = 'X'
                        st.session_state.current_player = 'O'
                        check_game_status()
                        if not st.session_state.game_over and not is_board_full(st.session_state.board):
                            ai_move()
            else:
                st.button(st.session_state.board[i][j], key=f"{i}{j}", disabled=True)

# Display game status
if st.session_state.game_over:
    if st.session_state.winner == 'X':
        st.success("You win! (That's impressive!)")
    elif st.session_state.winner == 'O':
        st.error("AI wins!")
    else:
        st.warning("It's a draw!")
    if st.button("Play Again"):
        reset_game()
        st.rerun()

# Instructions
st.markdown("""
### How to Play
- You are **X**, and the AI is **O**.
- Click an empty cell to make your move.
- The AI will respond instantly using the minimax algorithm, making it impossible to beat (but you can try for a draw!).
- The game ends when someone wins or the board is full.
- Click **Play Again** to start a new game.
""")