import socket
from threading import Thread

## Constants
HOST = socket.gethostbyname('localhost')
PORT = 65432
ADDR = (HOST,PORT)
FORMAT = 'utf-8'
BUFFER_SIZE = 1024
END_MESSAGE = 'end'

class ClientMessageHandler(Thread):
  REPLY_MESSAGE = b'Message received'

  def __init__(self, ip, port, sock):
    Thread.__init__(self)
    self.ip = ip
    self.port = port
    self.sock = sock
    print(f'New thread started for {ip}:{port}')
    
  def stop(self):
    if self.sock:
      sock.close()
  
  def run(self):
    try:
      with self.sock as sock:
        while True:
          data = sock.recv(BUFFER_SIZE).decode(FORMAT)
          if data == END_MESSAGE:
            sock.close()
            print(f'Client {ip}:{port} closed')
            break
          print(f'{self.ip}:{self.port} > {data}')
          sock.sendall(ClientMessageHandler.REPLY_MESSAGE)
    except ConnectionAbortedError:
      print(f'Client {ip}:{port} closed unexpectedly')

if __name__ == '__main__':
  tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  tcpsock.bind(ADDR)
  threads = []
  
  while True:
    try:
        tcpsock.listen(10)
        print('Waiting for incoming connections....')
        (conn, (ip, port)) = tcpsock.accept()
        print('Got connection from ', (ip, port))
        newthread = ClientMessageHandler(ip, port, conn)
        newthread.start()
        threads.append(newthread)
    except (SystemExit, KeyboardInterrupt) as e:
      print('Closing server...')
      for thread in threads:
        thread.stop()
        thread.join()