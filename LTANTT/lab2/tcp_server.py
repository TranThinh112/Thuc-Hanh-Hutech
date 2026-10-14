import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_ip = '127.0.0.1'  # Localhost
server_port = 8080

server_socket.bind((server_ip, server_port))
server_socket.listen(1)

print(f'Server đang lắng nghe tại {server_ip}:{server_port}')

conn, addr = server_socket.accept()
print(f'Kết nối từ {addr}')

conn.send(b'Hello, Client!')
data = conn.recv(1024)
print(f'Đã nhận: {data.decode()}')

conn.close()
server_socket.close()
