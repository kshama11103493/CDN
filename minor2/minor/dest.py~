import socket, struct

def main(host):
    # Connect to server and get image size.
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, 56712))
    packed = recvall(client, struct.calcsize('!I'))
    # Decode the size and get the image data.
    size = struct.unpack('!I', packed)[0]
    print('Receiving data from:', host)
    data = recvall(client, size)
    # Shutdown the socket and create the image file.
    client.shutdown(socket.SHUT_RDWR)
    client.close()
    with open('file.pdf', 'wb') as file:
        file.write(data)

def recvall(sock, size):
    message = bytearray()
    # Loop until all expected data is received.
    while len(message) < size:
        buffer = sock.recv(size - len(message))
        if not buffer:
            # End of stream was found when unexpected.
            raise EOFError('Could not receive all expected data!')
        message.extend(buffer)
    return bytes(message)

if __name__ == '__main__':
    main('10.42.0.1')
