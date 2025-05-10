Running the Game
To experience the concept:

Start the Server:
Run server.py in VS Code or a terminal.

Copy python server.py
See: Server running on 127.0.0.1:5555.

Now Start Two Clients:
In separate terminals, run client.py twice.

Copy python client.py
Player 1 sees a red rectangle, Player 2 sees a blue one, and both see each other’s movements.
Use arrow keys to move, observing real-time updates.
Test Networking:
Close one client to see the server log a disconnect and the other client update (only one rectangle remains).
Try running clients on different machines by updating HOST to the server’s IP (e.g., 192.168.1.100).