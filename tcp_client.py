import threading
import socket

# Choosing nickname
nickname = input("Choose your nickname: ")

# Connecting To server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 12345))

# Listening to server and sending nickname
def receive():
    while True:
        try:
            # If 'NICK' send nickname
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            # Close connection when error
            print("An error occured!")
            client.close()
            break

# Sending messages to server
def write():
    while True:
        text = input('')
        message = '{}: {}'.format(nickname, text)
        client.send(message.encode('ascii'))


# Starting threads For listening And writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()