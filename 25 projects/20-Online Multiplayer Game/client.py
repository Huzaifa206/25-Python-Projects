import pygame
import socket
import pickle
import threading
import asyncio
import platform

pygame.init()

# Window settings
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Multiplayer Game")
clock = pygame.time.Clock()

# Client settings
HOST = '127.0.0.1'
PORT = 5555
player_pos = [0, 0]
player_id = None
players = {}
running = True

def network_thread():
    global player_id, players, running, player_pos
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    
    # Receive initial player ID and game state
    data = client.recv(2048)
    player_id, players = pickle.loads(data)
    player_pos = players[player_id][:2]
    
    while running:
        try:
            # Send player position
            client.send(pickle.dumps(player_pos))
            
            # Receive updated game state
            data = client.recv(2048)
            if not data:
                break
            players = pickle.loads(data)
        except:
            break
    
    running = False
    client.close()

async def main():
    global player_pos, running
    # Start network thread
    threading.Thread(target=network_thread, daemon=True).start()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Handle movement
        keys = pygame.key.get_pressed()
        speed = 5
        if keys[pygame.K_LEFT]:
            player_pos[0] = max(0, player_pos[0] - speed)
        if keys[pygame.K_RIGHT]:
            player_pos[0] = min(WIDTH - 50, player_pos[0] + speed)
        if keys[pygame.K_UP]:
            player_pos[1] = max(0, player_pos[1] - speed)
        if keys[pygame.K_DOWN]:
            player_pos[1] = min(HEIGHT - 50, player_pos[1] + speed)
        
        # Draw
        screen.fill((0, 0, 0))  # Black background
        for p_id, (x, y, color) in players.items():
            pygame.draw.rect(screen, color, (x, y, 50, 50))
        
        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(1.0 / 60)
    
    pygame.quit()

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())