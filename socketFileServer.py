import socket
from os import path
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
    self._stop.set()
    
  def run(self):
    try:
      with self.sock as sock:
        with open(path.join('server', f'{ip}_{port}.txt'), 'wb') as f:
          while True:
            data = sock.recv(BUFFER_SIZE)
            f.write(data)
            if data == b'':
              sock.close()
              print(f'Client {ip}:{port} closed')
              return
          sock.sendall(ClientMessageHandler.REPLY_MESSAGE)
    except ConnectionAbortedError:
      print(f'Client {ip}:{port} closed unexpectedly')
      self.sock.close()
      return

if __name__ == '__main__':
  tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  tcpsock.bind(ADDR)
  threads = []
  
  try:
    while True:
      tcpsock.listen(10)
      print('Waiting for incoming connections....')
      (conn, (ip, port)) = tcpsock.accept()
      print('Got connection from ', (ip, port))
      newthread = ClientMessageHandler(ip, port, conn)
      newthread.start()
      threads.append(newthread)
  except KeyboardInterrupt as e:
    print('Closing server...')
    for thread in threads:
      thread.stop()
      thread.join()