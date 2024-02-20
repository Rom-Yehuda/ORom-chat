import threading
import socket

# Connection data
host = '127.0.0.1' # or "localhost"
port = 12345

# Starting server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
print("Server is UP!")


#{"A":1, "B": 2}
#{1: "A", 2:"B"}
# sockets 
# [s1, s2, s3]
# names
# [or, amot, yibal]

clients = []
nicknames = []


def broadcast(message):
    for client in clients:
        client.send(message)


# Handling messages from clients
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            # Removing and closing clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode('ascii'))
            nicknames.remove(nickname)
            break

# Receiving / listening messages
def receive():
    while True:
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Request and store nickname
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        # Print and broadcast nickname
        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('ascii'))
        client.send('Connected to server!'.encode('ascii'))

        # Start handling thread for client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

if __name__ == "__main__":
    receive()