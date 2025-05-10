import pygame
import random
import asyncio
import platform

# Initialize Pygame
pygame.init()

class Cube:
    rows = 20
    w = 500

    def __init__(self, start, dirnx=1, dirny=0, color=(255, 0, 0)):
        self.pos = start
        self.dirnx = dirnx
        self.dirny = dirny
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i, j = self.pos
        pygame.draw.rect(surface, self.color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))
        if eyes:
            centre = dis // 2
            radius = 3
            circleMiddle = (i * dis + centre - radius, j * dis + 8)
            circleMiddle2 = (i * dis + dis - radius * 2, j * dis + 8)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle2, radius)

class Snake:
    def __init__(self, color, pos):
        self.color = color
        self.head = Cube(pos)
        self.body = [self.head]
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and self.dirnx != 1:  # Prevent reversing
                self.dirnx, self.dirny = -1, 0
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
            elif keys[pygame.K_RIGHT] and self.dirnx != -1:
                self.dirnx, self.dirny = 1, 0
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
            elif keys[pygame.K_UP] and self.dirny != 1:
                self.dirnx, self.dirny = 0, -1
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
            elif keys[pygame.K_DOWN] and self.dirny != -1:
                self.dirnx, self.dirny = 0, 1
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                # Wrap around edges
                if c.dirnx == -1 and c.pos[0] <= 0:
                    c.pos = (c.rows - 1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows - 1:
                    c.pos = (0, c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows - 1:
                    c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows - 1)
                else:
                    c.move(c.dirnx, c.dirny)
        return True

    def reset(self, pos):
        self.head = Cube(pos)
        self.body = [self.head]
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def add_cube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny
        if dx == 1 and dy == 0:
            self.body.append(Cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(Cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] + 1)))
        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            c.draw(surface, i == 0)

def draw_grid(w, rows, surface):
    size_btwn = w // rows
    for l in range(rows):
        pygame.draw.line(surface, (255, 255, 255), (l * size_btwn, 0), (l * size_btwn, w))
        pygame.draw.line(surface, (255, 255, 255), (0, l * size_btwn), (w, l * size_btwn))

def random_snack(rows, snake):
    positions = [c.pos for c in snake.body]
    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if (x, y) not in positions:
            return (x, y)

async def main():
    global width, rows, win, snake, snack, score, game_over
    width = 500
    rows = 20
    win = pygame.display.set_mode((width, width))
    snake = Snake((255, 0, 0), (10, 10))
    snack = Cube(random_snack(rows, snake), color=(0, 255, 0))
    score = 0
    game_over = False
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Courier", 24)

    while True:
        if game_over:
            win.fill((0, 0, 0))
            game_over_text = font.render(f"Game Over! Score: {score}", True, (255, 255, 255))
            play_again_text = font.render("Press SPACE to Play Again", True, (255, 255, 255))
            win.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2, width // 2 - 20))
            win.blit(play_again_text, (width // 2 - play_again_text.get_width() // 2, width // 2 + 20))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    snake.reset((10, 10))
                    snack = Cube(random_snack(rows, snake), color=(0, 255, 0))
                    score = 0
                    game_over = False
            await asyncio.sleep(1.0 / 60)
            continue

        pygame.time.delay(50)
        clock.tick(10)
        if not snake.move():
            return

        # Check for snack collision
        if snake.body[0].pos == snack.pos:
            snake.add_cube()
            snack = Cube(random_snack(rows, snake), color=(0, 255, 0))
            score += 1

        # Check for self-collision
        for x in range(len(snake.body)):
            if snake.body[x].pos in [c.pos for c in snake.body[x + 1:]]:
                game_over = True
                break

        # Redraw window
        win.fill((0, 0, 0))
        snake.draw(win)
        snack.draw(win)
        draw_grid(width, rows, win)
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        win.blit(score_text, (10, 10))
        pygame.display.update()

        await asyncio.sleep(1.0 / 60)

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())