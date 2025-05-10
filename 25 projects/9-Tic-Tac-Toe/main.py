import streamlit as st

st.set_page_config(page_title="Tic-Tac-Toe", page_icon="🎲", layout="centered")

if "board" not in st.session_state:
    st.session_state.board = [[" " for _ in range(3)] for _ in range(3)]
    st.session_state.current_player = "X"
    st.session_state.game_over = False
    st.session_state.winner = None
    st.session_state.move_count = 0

st.title("Tic-Tac-Toe")
st.write("Play Tic-Tac-Toe! Players take turns as X and O. Click a square to make your move. First to get three in a row wins!")

def check_winner():
    board = st.session_state.board
  
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != " ":
            return board[i][0]
   
    for j in range(3):
        if board[0][j] == board[1][j] == board[2][j] != " ":
            return board[0][j]

    if board[0][0] == board[1][1] == board[2][2] != " ":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != " ":
        return board[0][2]
    return None

def make_move(i, j):
    if st.session_state.board[i][j] == " " and not st.session_state.game_over:
        st.session_state.board[i][j] = st.session_state.current_player
        st.session_state.move_count += 1
        
        winner = check_winner()
        if winner:
            st.session_state.game_over = True
            st.session_state.winner = winner
     
        elif st.session_state.move_count == 9:
            st.session_state.game_over = True
            st.session_state.winner = "Draw"
  
        else:
            st.session_state.current_player = "O" if st.session_state.current_player == "X" else "X"


def reset_game():
    st.session_state.board = [[" " for _ in range(3)] for _ in range(3)]
    st.session_state.current_player = "X"
    st.session_state.game_over = False
    st.session_state.winner = None
    st.session_state.move_count = 0

st.header(f"Current Player: {st.session_state.current_player}")

for i in range(3):
    cols = st.columns(3)
    for j in range(3):
        with cols[j]:
            
            label = st.session_state.board[i][j] if st.session_state.board[i][j] != " " else " "
            if st.button(label, key=f"cell_{i}_{j}", disabled=st.session_state.game_over or st.session_state.board[i][j] != " "):
                make_move(i, j)

if st.session_state.game_over:
    if st.session_state.winner == "Draw":
        st.warning("It's a Draw!")
    else:
        st.success(f"Player {st.session_state.winner} Wins!")

if st.button("New Game"):
    reset_game()

st.markdown("---")
st.write("Built with Streamlit | Enjoy the classic game!")