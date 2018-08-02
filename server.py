import socket
import serverconfig as config
import select
import struct
import json

def recv_msg(source_socket):
    buf = source_socket.recv(4096)
    cursor = 0
    buf_len = len(buf)
    while cursor < buf_len:
        message_length = struct.unpack('>I', buf[cursor:cursor+4])[0]
        cursor += 4 # 4 bytes
        if cursor + message_length == buf_len:
            return buf[cursor:]
        elif cursor + buf_len > buf_len:
            # receive next buffer
            buf = source_socket.recv(4096)
            cursor = 0
            buf_len = len(buf)

def 

def load_msg(source_data, source_address):


def main():
    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('', config.PORT))
    server_socket.listen(2)
    input_sockets = [server_socket]

    picameras_info = {}


    while True:
        input_fds = select.select(input_sockets, input_sockets, [], 2)[0]

        for fd in input_fds:
            if fd is server_socket:
                client_socket, client_address = fd.accept()
                input_sockets.append(client_socket)
                qu
                print("Connected to ", client_address)
            else:
                try:
                    data = recv_msg(fd)
                    source_address = fd.getpeername()[0]
                    source_data = json.loads(data.decode())
                    load_msg(source_data, source_address, bounds, camera_classes, picameras_info)
                except:
                    continue