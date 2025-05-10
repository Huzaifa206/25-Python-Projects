import numpy as np
import pygame
import sys
import math
import asyncio
import platform

# Colors
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Board dimensions
ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 2 - 5)
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Connect Four")

def create_board():
    return np.zeros((ROW_COUNT, COLUMN_COUNT))

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r
    return None

def winning_move(board, piece):
    # Horizontal
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if all(board[r][c + i] == piece for i in range(4)):
                return True
    # Vertical
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if all(board[r + i][c] == piece for i in range(4)):
                return True
    # Positive diagonal
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if all(board[r + i][c + i] == piece for i in range(4)):
                return True
    # Negative diagonal
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if all(board[r - i][c + i] == piece for i in range(4)):
                return True
    return False

def is_board_full(board):
    return not any(board[ROW_COUNT - 1][c] == 0 for c in range(COLUMN_COUNT))

def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, (r + 1) * SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (c * SQUARESIZE + SQUARESIZE / 2, (r + 1) * SQUARESIZE + SQUARESIZE / 2), RADIUS)
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (c * SQUARESIZE + SQUARESIZE / 2, height - (r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (c * SQUARESIZE + SQUARESIZE / 2, height - (r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)

async def main():
    global board, game_over, turn, score_p1, score_p2
    board = create_board()
    game_over = False
    turn = 0
    score_p1 = 0
    score_p2 = 0
    font = pygame.font.SysFont("monospace", 50)
    clock = pygame.time.Clock()

    while True:
        if game_over:
            screen.fill(BLACK)
            if winner == 1:
                text = font.render("Player 1 Wins!", True, RED)
            elif winner == 2:
                text = font.render("Player 2 Wins!", True, YELLOW)
            else:
                text = font.render("Tie Game!", True, (255, 255, 255))
            score_text = font.render(f"P1: {score_p1}  P2: {score_p2}", True, (255, 255, 255))
            replay_text = font.render("Press SPACE to Play Again", True, (255, 255, 255))
            screen.blit(text, (width // 2 - text.get_width() // 2, height // 2 - 60))
            screen.blit(score_text, (width // 2 - score_text.get_width() // 2, height // 2))
            screen.blit(replay_text, (width // 2 - replay_text.get_width() // 2, height // 2 + 60))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    board = create_board()
                    game_over = False
                    turn = 0
                    winner = 0
                    draw_board(board)
            await asyncio.sleep(1.0 / 60)
            continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.MOUSEMOTION and not game_over:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                posx = event.pos[0]
                color = RED if turn == 0 else YELLOW
                pygame.draw.circle(screen, color, (posx, SQUARESIZE / 2), RADIUS)
                pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                col = int(math.floor(event.pos[0] / SQUARESIZE))
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    piece = 1 if turn == 0 else 2
                    drop_piece(board, row, col, piece)
                    draw_board(board)

                    if winning_move(board, piece):
                        game_over = True
                        winner = piece
                        if piece == 1:
                            score_p1 += 1
                        else:
                            score_p2 += 1
                    elif is_board_full(board):
                        game_over = True
                        winner = 0

                    turn = (turn + 1) % 2

        score_text = font.render(f"P1: {score_p1}  P2: {score_p2}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        pygame.display.update()
        clock.tick(60)
        await asyncio.sleep(1.0 / 60)

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())