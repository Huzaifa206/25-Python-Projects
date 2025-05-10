import socket
import threading
import pickle

# Server settings
HOST = '127.0.0.1'  # localhost
PORT = 5555
WIDTH = 800
HEIGHT = 600

# Player data
players = {}  # {player_id: (x, y, color)}
player_id = 0
lock = threading.Lock()

def handle_client(conn, addr, p_id):
    global players
    print(f"New connection from {addr}, Player ID: {p_id}")
    
    # Assign initial position and color
    with lock:
        color = (255, 0, 0) if p_id == 0 else (0, 0, 255)  # Red for P1, Blue for P2
        players[p_id] = [100 + p_id * 100, 100, color]
    
    conn.send(pickle.dumps((p_id, players)))  # Send player ID and initial game state
    
    while True:
        try:
            # Receive player position
            data = conn.recv(2048)
            if not data:
                break
            player_pos = pickle.loads(data)
            
            # Update player position
            with lock:
                players[p_id][:2] = player_pos
                
            # Send updated game state to client
            conn.send(pickle.dumps(players))
        except:
            break
    
    # Remove player on disconnect
    with lock:
        del players[p_id]
    print(f"Player {p_id} disconnected")
    conn.close()

def main():
    global player_id
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(2)  # Support up to 2 players
    print(f"Server running on {HOST}:{PORT}")
    
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr, player_id))
        thread.start()
        player_id += 1

if __name__ == "__main__":
    main()