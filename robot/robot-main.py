import sys
import socket
import selectors
import types

# robot - 1: 100.75.56.66
# robot - 2: 100.92.112.53
# server: 100.107.15.32
# Robot-2 is the server and Robot-1 is the client **server is offline in this demo**
HOST = "100.107.15.32"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

def start_connections(host, port, num_conns):
    server_addr = (host, port)
    for i in range(0, num_conns):
        connid = i + 1
        #print(f"Starting connection to server")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex(server_addr)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        data = types.SimpleNamespace(
            connid=connid,
            msg_total=sum(len(m) for m in messages),
            recv_total=0,
            messages=messages.copy(),
            outb=b"",
        )
        sel.register(sock, events, data=data)

def service_connection(key, mask):
     sock = key.fileobj
     data = key.data
     if mask & selectors.EVENT_READ:
         recv_data = sock.recv(1024)  # Should be ready to read
         if recv_data:
            data.outb += recv_data
            print("Received")
            data.recv_total += len(recv_data)
         else:
            print("Closing connection")
         if not recv_data or data.recv_total == data.msg_total:
            print("Closing connection")
            sel.unregister(sock)
            sock.close()
     if mask & selectors.EVENT_WRITE:
        if not data.outb and data.messages:
            data.outb = data.messages.pop(0)
        if data.outb:
            print("Echoing  to")
            print("Sending  to connections")
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]

#with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#    s.connect((HOST, PORT))
#    s.sendall(b"Hello, world")
#    data = s.recv(1024)

#print(f"Received {data!r}")
sel = selectors.DefaultSelector()
messages = [b"Message 1 from client.", b"Message 2 from client."]
start_connections(HOST, PORT, 2)
print("made it here")
