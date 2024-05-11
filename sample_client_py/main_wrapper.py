import io
import socket
import sys

PORT = 8888

class SocketIO(io.RawIOBase):
  def __init__(self, sock):
    self.sock = sock
  def read(self, sz=-1):
    if sz == -1:
      sz = 0x7FFFFFFF
    return self.sock.recv(sz)
  def write(self, b):
    self.sock.sendall(b)
  def readable(self):
    return True
  def writable(self):
    return True
  def seekable(self):
    return False

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
  try:
    sock.connect(('127.0.0.1', PORT))
  except:
    sys.exit(1)
  with io.TextIOWrapper(SocketIO(sock), 'utf-8') as sio:
    # 標準入出力を置き換え
    sys.stdin = sio
    sys.stdout = sio

    # プログラム本体の実行
    import main

    sys.stdin = sys.__stdin__
    sys.stdout = sys.__stdout__
