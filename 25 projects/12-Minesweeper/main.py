import streamlit as st
import random
import numpy as np

# Initialize session state
if 'board' not in st.session_state:
    st.session_state.board = None
    st.session_state.game_over = False
    st.session_state.won = False
    st.session_state.flags = None

class Board:
    def __init__(self, dim_size, num_bombs):
        self.dim_size = dim_size
        self.num_bombs = num_bombs
        self.board = self.make_new_board()
        self.assign_values_to_board()
        self.dug = set()

    def make_new_board(self):
        board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        bombs_planted = 0
        while bombs_planted < self.num_bombs:
            loc = random.randint(0, self.dim_size**2 - 1)
            row = loc // self.dim_size
            col = loc % self.dim_size
            if board[row][col] == '*':
                continue
            board[row][col] = '*'
            bombs_planted += 1
        return board

    def assign_values_to_board(self):
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if self.board[r][c] == '*':
                    continue
                self.board[r][c] = self.get_num_neighboring_bombs(r, c)

    def get_num_neighboring_bombs(self, row, col):
        num_neighboring_bombs = 0
        for r in range(max(0, row-1), min(self.dim_size-1, row+1)+1):
            for c in range(max(0, col-1), min(self.dim_size-1, col+1)+1):
                if r == row and c == col:
                    continue
                if self.board[r][c] == '*':
                    num_neighboring_bombs += 1
        return num_neighboring_bombs

    def dig(self, row, col):
        self.dug.add((row, col))
        if self.board[row][col] == '*':
            return False
        elif self.board[row][col] > 0:
            return True
        for r in range(max(0, row-1), min(self.dim_size-1, row+1)+1):
            for c in range(max(0, col-1), min(self.dim_size-1, col+1)+1):
                if (r, c) in self.dug:
                    continue
                self.dig(r, c)
        return True

    def __str__(self):
        visible_board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if (row,col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = ' '
        string_rep = ''
        widths = []
        for idx in range(self.dim_size):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(len(max(columns, key=len)))
        indices = [i for i in range(self.dim_size)]
        indices_row = '   '
        cells = []
        for idx, col in enumerate(indices):
            format = '%-' + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row += '  '.join(cells)
        indices_row += '  \n'
        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f'{i} |'
            cells = []
            for idx, col in enumerate(row):
                format = '%-' + str(widths[idx]) + "s"
                cells.append(format % (col))
            string_rep += ' |'.join(cells)
            string_rep += ' |\n'
        str_len = int(len(string_rep) / self.dim_size)
        string_rep = indices_row + '-'*str_len + '\n' + string_rep + '-'*str_len
        return string_rep

# Streamlit UI
st.title("🎮 Minesweeper")
st.subheader("Uncover safe cells, avoid the mines!")

# Game settings
dim_size, num_bombs = 10, 10
if st.session_state.board is None:
    st.session_state.board = Board(dim_size, num_bombs)
    st.session_state.flags = np.zeros((dim_size, dim_size), dtype=bool)

# Game board container
with st.container():
    st.write("**Game Board**")
    board = st.session_state.board
    # Display column indices
    col_indices = st.columns(dim_size)
    for c in range(dim_size):
        with col_indices[c]:
            st.markdown(f"**{c}**", unsafe_allow_html=True)
    
    for r in range(board.dim_size):
        row_cols = st.columns([1] + [1] * dim_size)  # First column for row index
        with row_cols[0]:
            st.markdown(f"**{r}**", unsafe_allow_html=True)
        for c in range(board.dim_size):
            with row_cols[c + 1]:
                if (r, c) in board.dug:
                    if board.board[r][c] == '*':
                        label = "💥"
                    elif board.board[r][c] == 0:
                        label = "⬜"
                    else:
                        label = str(board.board[r][c])
                    st.button(label, key=f"cell_{r}_{c}", disabled=True)
                elif st.session_state.flags[r, c]:
                    st.button("🚩", key=f"cell_{r}_{c}", disabled=True)
                else:
                    if st.button("⬛", key=f"cell_{r}_{c}") and not st.session_state.game_over:
                        safe = board.dig(r, c)
                        if not safe:
                            st.session_state.game_over = True
                        elif len(board.dug) >= board.dim_size ** 2 - board.num_bombs:
                            st.session_state.game_over = True
                            st.session_state.won = True
                        st.rerun()

                # Flag checkbox
                flag = st.checkbox("🚩", key=f"flag_{r}_{c}", value=st.session_state.flags[r, c])
                if flag != st.session_state.flags[r, c] and not st.session_state.game_over:
                    st.session_state.flags[r, c] = flag
                    st.rerun()

# Game status
if st.session_state.game_over:
    if st.session_state.won:
        st.balloons()
        st.success("🎉 CONGRATULATIONS! YOU WON!")
    else:
        st.error("💣 GAME OVER! You hit a mine.")
        board.dug = [(r, c) for r in range(board.dim_size) for c in range(board.dim_size)]
    if st.button("🔄 New Game"):
        st.session_state.board = Board(dim_size, num_bombs)
        st.session_state.flags = np.zeros((dim_size, dim_size), dtype=bool)
        st.session_state.game_over = False
        st.session_state.won = False
        st.rerun()

# Instructions in an expander for cleaner UI
with st.expander("📜 How to Play"):
    st.markdown("""
    ### How to Play
    - **Objective**: Reveal all safe cells (90) without hitting any of the 10 mines.
    - Click a black square (⬛) to dig:
      - **Number**: Shows how many mines are adjacent.
      - **Empty (⬜)**: Recursively reveals adjacent cells if no adjacent mines.
      - **Mine (💥)**: Ends the game.
    - Check the **Flag** box to mark suspected mines (🚩).
    - Win by revealing all non-mine cells.
    - Click **New Game** to restart.

    ### About the Game
    - **Grid**: 10x10 with 10 mines.
    - **Classes**: The `Board` class manages the game state.
    - **Recursion**: Used in `dig` to reveal adjacent cells for empty spots.
    - **Adapted from Kylie Ying's command-line Minesweeper.**
    """)

# Display remaining cells to reveal
remaining = board.dim_size ** 2 - board.num_bombs - len(board.dug)
st.metric("Cells to Reveal", remaining)