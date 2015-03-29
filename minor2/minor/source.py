import os, struct, socket

def main():
    # Take screenshot and load the data.
    os.system('scrot file.pdf')
    with open('file.pdf', 'rb') as file:
        data = file.read()
    # Construct message with data size.
    size = struct.pack('!I', len(data))
    message = size + data
    # Open up a server socket.
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('10.42.0.73', 56712))
    server.listen(5)
    # Constantly server incoming clients.
    while True:
        client, address = server.accept()
        print('Sending data to:', address)
        # Send the data and shutdown properly.
        client.sendall(message)
        client.shutdown(socket.SHUT_RDWR)
        client.close()

if __name__ == '__main__':
    main()


