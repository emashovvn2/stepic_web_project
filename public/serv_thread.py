import errno
import threading
import socket
BIND_ADDRESS = ('', 2222)
BACKLOG = 1

def handle(sock, clinet_ip, client_port):
    data = sock.recv(1024)
    if data != 'close':
        sock.sendall(data)
    sock.close()

def serve_forever():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(BIND_ADDRESS)
    sock.listen(BACKLOG)
    while True:
        try:
            connection, (client_ip, clinet_port) = sock.accept()
        except IOError as e:
            if e.errno == errno.EINTR:
                continue
            raise
        thread = threading.Thread(
            target=handle,
            args=(connection, client_ip, clinet_port)
        )
        thread.daemon = True
        thread.start()
serve_forever()
