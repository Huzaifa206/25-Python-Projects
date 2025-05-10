import streamlit as st
import numpy as np
from copy import deepcopy
from pprint import pprint

# Sudoku solver functions
def find_next_empty(puzzle):
    for r in range(9):
        for c in range(9):
            if puzzle[r][c] == -1:
                return r, c
    return None, None

def is_valid(puzzle, guess, row, col):
    row_vals = puzzle[row]
    if guess in row_vals:
        return False
    col_vals = [puzzle[i][col] for i in range(9)]
    if guess in col_vals:
        return False
    row_start = (row // 3) * 3
    col_start = (col // 3) * 3
    for r in range(row_start, row_start + 3):
        for c in range(col_start, col_start + 3):
            if puzzle[r][c] == guess:
                return False
    return True

def solve_sudoku(puzzle):
    row, col = find_next_empty(puzzle)
    if row is None:
        return True
    for guess in range(1, 10):
        if is_valid(puzzle, guess, row, col):
            puzzle[row][col] = guess
            if solve_sudoku(puzzle):
                return True
        puzzle[row][col] = -1
    return False

st.title("🎲 Sudoku Solver")
st.subheader("Enter a Sudoku puzzle and solve it with backtracking!")

# Initialize session state
if 'puzzle' not in st.session_state:
    st.session_state.puzzle = [[-1 for _ in range(9)] for _ in range(9)]
if 'solved' not in st.session_state:
    st.session_state.solved = False
if 'solution' not in st.session_state:
    st.session_state.solution = None

st.write("**Enter Puzzle (use 1-9 for numbers, leave empty for blanks)**")
with st.form("sudoku_form"):
    puzzle = []
    for r in range(9):
        cols = st.columns(9)
        row = []
        for c in range(9):
            with cols[c]:
                # Use text_input for single-digit entry
                value = st.text_input("", key=f"cell_{r}_{c}", max_chars=1, value="" if st.session_state.puzzle[r][c] == -1 else str(st.session_state.puzzle[r][c]))
                if value == "" or value == "-":
                    row.append(-1)
                else:
                    try:
                        num = int(value)
                        if 1 <= num <= 9:
                            row.append(num)
                        else:
                            row.append(-1)
                    except ValueError:
                        row.append(-1)
        puzzle.append(row)
    submitted = st.form_submit_button("Solve")
    clear = st.form_submit_button("Clear")

if clear:
    st.session_state.puzzle = [[-1 for _ in range(9)] for _ in range(9)]
    st.session_state.solved = False
    st.session_state.solution = None
    st.rerun()

if submitted:
    st.session_state.puzzle = puzzle
    puzzle_copy = deepcopy(puzzle)  # Work on a copy to avoid modifying input
    if solve_sudoku(puzzle_copy):
        st.session_state.solution = puzzle_copy
        st.session_state.solved = True
    else:
        st.session_state.solved = False
        st.session_state.solution = None
    st.rerun()

if st.session_state.solved and st.session_state.solution:
    st.success("Puzzle solved!")
    st.write("**Solution**")
    for r in range(9):
        cols = st.columns(9)
        for c in range(9):
            with cols[c]:
                value = st.session_state.solution[r][c]
                st.markdown(f"**{value}**", unsafe_allow_html=True)
elif submitted and not st.session_state.solved:
    st.error("This puzzle is unsolvable!")

with st.expander("📜 How to Play"):
    st.markdown("""
    ### How to Use
    - Enter a 9x9 Sudoku puzzle in the grid:
      - Use numbers **1-9** for filled cells.
      - Leave cells blank (or enter '-') for empty cells.
    - Click **Solve** to find the solution using backtracking.
    - Click **Clear** to reset the grid.
    - The solution (if solvable) will be displayed below.

    ### About the Solver
    - **Algorithm**: Uses backtracking, a recursive technique that tries all possible numbers (1-9) for each empty cell, ensuring Sudoku rules are followed.
    - **Rules**: Each number (1-9) must appear at most once in each row, column, and 3x3 subgrid.
    - **Features**:
      - Finds the next empty cell.
      - Validates guesses for rows, columns, and 3x3 squares.
      - Backtracks if a guess leads to an invalid state.
    - **Inspired by a classic Sudoku solver implementation.**
    """)